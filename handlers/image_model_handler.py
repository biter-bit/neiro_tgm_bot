from aiogram import Router, F
from aiogram.types import Message, FSInputFile, URLInputFile, CallbackQuery

from db_api.models import ImageQuery
from db_api.models import Profile
from utils.enum import AiModelName, MjOption
from db_api import api_chat_session_async, api_image_query_async
from utils.features import (finish_generation_image, get_image_part, create_safe_filename, check_access_for_generic,
                            make_request, create_photo, delete_image)
from services import nlp_translator, midjourney_obj
from utils.states import TypeAiState
from utils.features import get_session_for_profile
import asyncio
from utils.callbacks import MJCallback
from buttons.mjoption_ib import create_inline_kb_for_image
from config import settings
from services import logger
import re
from utils.enum import Errors
import json
from utils.cache import set_cache_profile
from aiogram.exceptions import TelegramMigrateToChat

image_router = Router()

async def check_task_mj(message: Message, result_task_generic: dict, user_profile: Profile, image_query: ImageQuery, msg: Message):
    while True:
        result_task = await midjourney_obj.async_get_result_task(result_task_generic["result"])
        download_percentage = result_task['result']['content']
        match = re.search(r'\((\d+%)\)', download_percentage)
        new_text = f"🖌️ Рисуем Ваше изображение... {match.group(1) if match else ''}"
        if match and new_text != msg.text:
            msg = await message.bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=msg.message_id,
                text=f"🖌️ Рисуем Ваше изображение... {match.group(1)}"
            )
        if result_task['status_code'] != 200:
            logger.error(result_task_generic['result'])
            await message.answer("❌ Во время генерации произошла ошибка. Попробуйте написать запрос заново.")
            break
        if result_task["result"]['status'] == 'completed':
            caption = "V - сделать еще 4 похожих изображения на конкретную картинку.\nU - выдать конкретное изображение в большом разрешении."
            inline_kb = create_inline_kb_for_image(image_query.id)
            await message.bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
            await message.answer_photo(
                URLInputFile(result_task["result"]['attachments'][0]['url']),
                caption=caption,
                reply_markup=inline_kb
            )
            profile = await finish_generation_image(
                url_photo=result_task["result"]['attachments'][0]['url'], profile=user_profile,
                image_id=image_query.id
            )
            await set_cache_profile(profile.tgid, json.dumps(profile.to_dict()))
            break
        await asyncio.sleep(5)
    return "Ok"

@image_router.message(TypeAiState.image)
async def generate_image_model(message: Message, user_profile: Profile):
    """Сгенерируй изображение по запросу"""
    session_profile = await get_session_for_profile(user_profile, user_profile.ai_model_id)
    access_to_generic = check_access_for_generic(user_profile, session_profile)
    if access_to_generic["status"] != Errors.NON_ERROR.name:
        logger.info(access_to_generic["result"])
        if access_to_generic["status"] == Errors.ERROR_ACTIVE_GENERATE.name:
            try:
                return await message.answer("🪄 Генерация для данной модели уже активна.")
            except TelegramMigrateToChat as e:
                logger.error(f"Чат был обновлён. Обработай ошибку: {e}")
        return await message.answer("❌ На балансе недостаточно средств или выбран недоступный тариф.")

    msg = await message.answer("Переводим ваш запрос...")
    if user_profile.ai_model_id in (AiModelName.MIDJOURNEY_5_2.value, AiModelName.MIDJOURNEY_6_0.value):
        try:
            await api_chat_session_async.active_generic_in_session(session_profile.id)

            result_translate = await nlp_translator.async_translate(text=message.text)
            if result_translate["status"] == "error":
                logger.error(result_translate['result'])
                await message.bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
                return await message.answer("❌ Во время генерации произошла ошибка. Попробуйте написать запрос заново.")

            version_mj = "6.0" if session_profile.ai_model_id == AiModelName.MIDJOURNEY_6_0.value else "5.2"
            result_task_generic = await midjourney_obj.async_generate_image(result_translate['result'], version_mj)
            if result_task_generic['status_code'] != 200:
                logger.error(result_task_generic["result"])
                await message.bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
                return await message.answer("❌ Во время генерации произошла ошибка. Попробуйте написать запрос заново.")

            image_query = await api_image_query_async.create_image_query(
                result_task_generic["result"]['prompt'], session_profile.id, result_task_generic["result"]['jobid']
            )

            msg = await message.bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=msg.message_id,
                text="🚶‍♂️🚶‍♀️ Ваш запрос в очереди на генерацию..."
            )
            await check_task_mj(message, result_task_generic, user_profile, image_query, msg)
        except Exception as e:
            logger.error(e)
        finally:
            await api_chat_session_async.deactivate_generic_in_session(session_profile.id)

@image_router.callback_query(MJCallback.filter(F.action == MjOption.VARIATION))
async def generate_variation_image_model(query: CallbackQuery, user_profile: Profile, callback_data: MJCallback):
    session_profile = await get_session_for_profile(user_profile, user_profile.ai_model_id)
    text_button = f"{'V'}{callback_data.index}"
    query_id = callback_data.mj_query_id.hex

    access_to_generic = check_access_for_generic(user_profile, session_profile)
    if access_to_generic["status"] != Errors.NON_ERROR.name:
        logger.info(access_to_generic["result"])
        if access_to_generic["status"] == Errors.ERROR_ACTIVE_GENERATE.name:
            return await query.message.answer("🪄 Генерация для данной модели уже активна.")
        return await query.message.answer("❌ На балансе недостаточно средств или выбран недоступный тариф.")

    msg = await query.message.answer("Переводим ваш запрос...")

    try:
        await api_chat_session_async.active_generic_in_session(session_profile.id)
        image_query = await api_image_query_async.get_image_query(query_id)
        result_task_generic = await midjourney_obj.async_get_variation_image(image_query.jobid, text_button)

        if result_task_generic['status_code'] != 200:
            logger.error(result_task_generic["result"])
            await query.message.bot.delete_message(chat_id=query.message.chat.id, message_id=msg.message_id)
            return await query.message.answer("❌ Во время генерации произошла ошибка. Попробуйте написать запрос заново.")

        image_query = await api_image_query_async.create_image_query(image_query.query, session_profile.id, result_task_generic["result"]['jobid'])

        msg = await query.message.bot.edit_message_text(
            chat_id=query.message.chat.id,
            message_id=msg.message_id,
            text="🚶‍♂️🚶‍♀️ Ваш запрос в очереди на генерацию..."
        )

        await check_task_mj(query.message, result_task_generic, user_profile, image_query, msg)
    except Exception as e:
        logger.error(e)
    finally:
        await api_chat_session_async.deactivate_generic_in_session(session_profile.id)


@image_router.callback_query(MJCallback.filter(F.action == MjOption.UPSAMPLE))
async def generate_variation_image_model(query: CallbackQuery, user_profile: Profile, callback_data: MJCallback):
    session_profile = await get_session_for_profile(user_profile, user_profile.ai_model_id)
    text_button = f"{'V'}{callback_data.index}"
    query_id = callback_data.mj_query_id.hex

    access_to_generic = check_access_for_generic(user_profile, session_profile)
    if access_to_generic["status"] != Errors.NON_ERROR.name:
        logger.info(access_to_generic["result"])
        if access_to_generic["status"] == Errors.ERROR_ACTIVE_GENERATE.name:
            return await query.message.answer("🪄 Генерация для данной модели уже активна.")
        return await query.message.answer("❌ На балансе недостаточно средств или выбран недоступный тариф.")

    await api_chat_session_async.active_generic_in_session(session_profile.id)

    image_query = await api_image_query_async.get_image_query(query_id)

    try:
        result = await make_request(image_query.answer)
        name_file = create_safe_filename(image_query.answer)

        if result["status_code"] != 200:
            logger.error(result["result"])
            return await query.message.answer("❌ Во время генерации произошла ошибка. Попробуйте написать запрос заново.")

        path_result = f"{settings.PATH_WORK}/mj_results/{name_file}"
        create_photo(photo_byte=result["result"].content, path_file=path_result)
        path_cut_photo = get_image_part(path_result, callback_data.index, f'{settings.PATH_WORK}/mj_results/',
                                     f"{text_button} - {name_file}")

        if path_cut_photo:
            await query.message.answer_photo(photo=FSInputFile(path_cut_photo))
            await query.message.answer_document(document=FSInputFile(path_cut_photo))
            # await api_profile_async.subtracting_count_request_to_model_mj(user_profile.id)
        else:
            await query.message.answer("❌ Во время генерации произошла ошибка. Попробуйте написать запрос заново.")
        delete_image(path_cut_photo)
        delete_image(path_result)
    except Exception as e:
        logger.error(e)
    finally:
        await api_chat_session_async.deactivate_generic_in_session(session_profile.id)