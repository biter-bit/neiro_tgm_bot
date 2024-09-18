from aiogram import Router, F
from aiogram.types import Message, FSInputFile, URLInputFile, CallbackQuery
from tgbot_app.db_api.models import Profile, ChatSession
from utils.enum import AiModelName, MjOption, Errors
from db_api import api_chat_session_async, api_profile_async, api_image_query_async
from utils.features import finish_generation_image, get_image_part, create_safe_filename, check_access_for_generic
from services import nlp_translator, midjourney_obj
from aiogram.fsm.context import FSMContext
from states.type_generation import TypeState
import httpx
import asyncio
from utils.callbacks import MJCallback
from buttons.mjoption_ib import create_inline_kb_for_image
from services import bot
from tgbot_app import settings
from tgbot_app.services import logger

image_router = Router()

@image_router.message(TypeState.image)
async def generate_image_model(message: Message, user_profile: Profile, state: FSMContext, session_profile: ChatSession):
    """Сгенерируй изображение по запросу"""
    access_to_generic = check_access_for_generic(user_profile, session_profile)
    if not access_to_generic["status"]:
        logger.info(access_to_generic["result"])
        return await message.answer("❌ На балансе недостаточно средств или выбран недоступный тариф.")

    if user_profile.ai_model_id == AiModelName.MIDJOURNEY.value:
        try:
            await api_chat_session_async.active_generic_in_session(session_profile.id)

            result_translate = await nlp_translator.async_translate(text=message.text)
            if result_translate["status"] == "error":
                logger.error(result_translate['result'])
                return await message.answer("❌ Во время генерации произошла ошибка. Попробуйте написать запрос заново.")

            result_task_generic = await midjourney_obj.async_generate_image(result_translate['result'])
            if result_task_generic['status_code'] != 200:
                logger.error(result_task_generic["result"])
                return await message.answer("❌ Во время генерации произошла ошибка. Попробуйте написать запрос заново.")

            image_query = await api_image_query_async.create_image_query(
                result_task_generic["result"]['prompt'], session_profile.id, result_task_generic["result"]['jobid']
            )

            while True:
                result_task = await midjourney_obj.async_get_result_task(result_task_generic["result"])
                if result_task['status_code'] != 200:
                    logger.error(result_task_generic['result'])
                    await message.answer("❌ Во время генерации произошла ошибка. Попробуйте написать запрос заново.")
                    break
                if result_task["result"]['status'] == 'completed':
                    inline_kb = create_inline_kb_for_image(image_query.id)
                    await message.answer_photo(
                        URLInputFile(result_task["result"]['attachments'][0]['url']),
                        caption='Вот изображение!',
                        reply_markup=inline_kb
                    )
                    await finish_generation_image(
                        url_photo=result_task["result"]['attachments'][0]['url'], profile_id=user_profile.id,
                        image_id=image_query.id
                    )
                    break
                await asyncio.sleep(5)
        except Exception as e:
            logger.error(e)
        finally:
            await api_chat_session_async.deactivate_generic_in_session(session_profile.id)

@image_router.callback_query(MJCallback.filter(F.action == MjOption.VARIATION))
async def generate_variation_image_model(query: CallbackQuery, user_profile: Profile, state: FSMContext, session_profile: ChatSession):
    info_query = query.data.split(':')
    text_button = f"{'V'}{info_query[2]}"
    query_id = info_query[3]

    access_to_generic = check_access_for_generic(user_profile, session_profile)
    if not access_to_generic["status"]:
        logger.info(access_to_generic["result"])
        return await query.message.answer("❌ На балансе недостаточно средств или выбран недоступный тариф.")

    try:
        await api_chat_session_async.active_generic_in_session(session_profile.id)
        image_query = await api_image_query_async.get_image_query(query_id)
        result_task_generic = await midjourney_obj.async_get_variation_image(image_query.jobid, text_button)

        if result_task_generic['status_code'] != 200:
            logger.error(result_task_generic["result"])
            return await query.message.answer("❌ Во время генерации произошла ошибка. Попробуйте написать запрос заново.")

        image_query = await api_image_query_async.create_image_query(image_query.query, session_profile.id, result_task_generic["result"]['jobid'])
        while True:
            result_task = await midjourney_obj.async_get_result_task(result_task_generic["result"])
            if result_task['status_code'] != 200:
                logger.error(result_task_generic['result'])
                await query.message.answer("❌ Во время генерации произошла ошибка. Попробуйте написать запрос заново.")
                break
            if result_task["result"]['status'] == 'completed':
                inline_kb = create_inline_kb_for_image(image_query.id)
                await query.message.answer_photo(
                    URLInputFile(result_task["result"]['attachments'][0]['url']),
                    caption='Вот изображение!',
                    reply_markup=inline_kb
                )
                await finish_generation_image(
                    url_photo=result_task["result"]['attachments'][0]['url'], profile_id=user_profile.id,
                    image_id=image_query.id
                )
                break
            await asyncio.sleep(5)
    except Exception as e:
        logger.error(e)
    finally:
        await api_chat_session_async.deactivate_generic_in_session(session_profile.id)


@image_router.callback_query(MJCallback.filter(F.action == MjOption.UPSAMPLE))
async def generate_variation_image_model(query: CallbackQuery, user_profile: Profile, state: FSMContext, session_profile: ChatSession):
    info_query = query.data.split(':')
    text_button = info_query[2]
    query_id = info_query[3]
    image_query = await api_image_query_async.get_image_query(query_id)

    access_to_generic = check_access_for_generic(user_profile, session_profile)
    if not access_to_generic["status"]:
        logger.info(access_to_generic["result"])
        return await query.message.answer("❌ На балансе недостаточно средств или выбран недоступный тариф.")

    await api_chat_session_async.active_generic_in_session(session_profile.id)

    async with httpx.AsyncClient() as client:
        result = await client.get(image_query.answer)
    name_file = create_safe_filename(image_query.answer)
    # Проверяем успешность запроса
    if result.status_code == 200:
        # Указываем путь, где будет сохранено изображение
        path_result = f"{settings.PATH_WORK}/mj_results/{name_file}"

        # Открываем файл для записи в бинарном режиме и сохраняем содержимое
        with open(path_result, 'wb') as image_file:
            image_file.write(result.content)

        path_result = get_image_part(path_result, int(text_button), f'{settings.PATH_WORK}/mj_results/',
                                     f"{text_button} - {name_file}")
        if path_result:
            await query.message.answer_photo(photo=FSInputFile(path_result))
            await query.message.answer_document(document=FSInputFile(path_result))
            await api_profile_async.subtracting_count_request_to_model_mj(user_profile.id)
        else:
            await query.message.answer("Что-то пошло не так!")
    else:
        # Обработка ошибки, если запрос не удался
        raise ValueError("Ошибка при загрузке изображения.")
    await api_chat_session_async.deactivate_generic_in_session(session_profile.id)