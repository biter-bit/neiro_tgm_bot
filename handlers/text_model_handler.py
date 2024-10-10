from aiogram import Router, F
from aiogram.types import Message, ContentType

from db_api.models import ChatSession
from db_api.models import Profile
from utils.enum import AiModelName, Messages
from db_api import api_chat_session_async, api_text_query_async, api_profile_async
from services import chat_gpt, redis, logger, bot
from openai import BadRequestError
from .image_model_handler import generate_image_model
from utils.features import check_limits_for_free_tariff, check_balance_profile
from aiogram.fsm.context import FSMContext
from states.type_generation import TypeState
import json
from io import BytesIO
import base64

text_router = Router()

text_models_openai = [
    AiModelName.GPT_4_O_MINI.value, AiModelName.GPT_4_O.value, AiModelName.GPT_O1_MINI.value,
    AiModelName.GPT_O1_PREVIEW.value
]


@text_router.message(F.content_type == ContentType.PHOTO)
async def handle_photo(message: Message, user_profile: Profile, session_profile: ChatSession):
    current_model = user_profile.ai_model_id
    if current_model == AiModelName.GPT_4_O.value:
        if session_profile.active_generation:
            await message.delete()
            return await message.answer('Генерация активна')

        if user_profile.tariffs.name == "Free" and user_profile.ai_model_id in ("gpt-4o", "o1-mini", "o1-preview"):
            return await message.answer("Для доступа к этой модели поменяйте тариф!")
        if not check_limits_for_free_tariff(user_profile):
            return await message.answer("Вы превысили лимит запросов в сутки для этой модели!")
        photo = message.photo[-1]  # Берем фото с максимальным разрешением
        file_info = await bot.get_file(photo.file_id)

        # Загружаем фото в байты
        file = await bot.download_file(file_info.file_path)

        # Читаем данные и кодируем в base64
        buffer = BytesIO(file.read())
        encoded_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

        try:
            message_dict = json.dumps({'type': 'text', 'text': message.md_text})
            photo_dict = json.dumps({'type': 'image_url', 'image_url': {"url": f"data:image/jpeg;base64,{encoded_image}"}})
            await api_chat_session_async.active_generic_in_session(session_profile.id)
            # text_query = await api_text_query_async.create_text_query(f"{message_dict},{photo_dict}", session_profile.id)
            text_messages = await api_chat_session_async.get_text_messages_from_session(session_profile.id,
                                                                                        current_model)
            deserialization_list = [json.loads(message_dict), json.loads(photo_dict)]
            response = await chat_gpt.async_generate_image_to_text(
                ai_model=current_model, context=text_messages, prompt=deserialization_list
            )
            # await api_text_query_async.save_message(response.choices[0].message.content, text_query.id)
            await message.reply(f"{response.choices[0].message.content}")

            if user_profile.ai_model_id == AiModelName.GPT_4_O.value and user_profile.chatgpt_4o_daily_limit > 0:
                profile = await api_profile_async.subtracting_count_request_to_model_gpt(user_profile.id,
                                                                                         user_profile.ai_model_id)
                await redis.set(user_profile.tgid, json.dumps(profile.to_dict()))
            await api_chat_session_async.deactivate_generic_in_session(session_profile.id)
        except BadRequestError as error:
            logger.error(error)
            await api_chat_session_async.deactivate_generic_in_session(session_profile.id)
            await api_chat_session_async.delete_context_from_session(session_profile.id, user_profile)
            await message.answer(Messages.ERROR.value)
            if error.code == "context_length_exceeded":
                # logger.error("BadRequestError error | MAX CONTEXT")
                return {"status": "error", "code": "max_content", "result": "Превышен контекст"}

            # logger.error(f"BadRequestError error | {error}  {error.code}")
            await message.answer(Messages.ERROR.value)
            return {"status": "error", "code": error.code, "result": ""}

        except Exception as error:
            logger.error(error)
            await api_chat_session_async.deactivate_generic_in_session(session_profile.id)
            await api_chat_session_async.delete_context_from_session(session_profile.id, user_profile)
            await message.answer(Messages.ERROR.value)
            if error.code == "context_length_exceeded":
                # logger.error("BadRequestError error | MAX CONTEXT")
                return {"status": "error", "code": "max_content", "result": "Превышен контекст"}
            return {"status": "error", "code": error.code, "result": ""}
    else:
        await message.answer("Похоже, что вы прикрепили изображение. Считывание изображений доступно в GPT-4o. "
                             "Выберите языковую модель по команде /mode")

@text_router.message(TypeState.text)
async def generate_text_model(message: Message, user_profile: Profile, session_profile: ChatSession):
    """Обработай текстовые сообщения пользователей, которые являются prompt для текстовых нейронок"""
    if user_profile.ai_model_id in text_models_openai:
        if session_profile.active_generation:
            await message.delete()
            return await message.answer('Генерация активна')

        current_model = user_profile.ai_model_id

        if user_profile.tariffs.name == "Free" and user_profile.ai_model_id in ("gpt-4o", "o1-mini", "o1-preview"):
            return await message.answer("Для доступа к этой модели поменяйте тариф!")
        if not check_limits_for_free_tariff(user_profile):
            return await message.answer("Вы превысили лимит запросов в сутки для этой модели!")

        try:
            if current_model in text_models_openai:
                await api_chat_session_async.active_generic_in_session(session_profile.id)
                text_query = await api_text_query_async.create_text_query(message.text, session_profile.id)
                text_messages = await api_chat_session_async.get_text_messages_from_session(session_profile.id, current_model)
                response = await chat_gpt.async_generate_text(
                    ai_model=current_model, context=text_messages, prompt=message.text
                )
                await api_text_query_async.save_message(response.choices[0].message.content, text_query.id)
                await message.answer(f"{response.choices[0].message.content}")

                if user_profile.ai_model_id == AiModelName.GPT_4_O.value and user_profile.chatgpt_4o_daily_limit > 0:
                    profile = await api_profile_async.subtracting_count_request_to_model_gpt(user_profile.id, user_profile.ai_model_id)
                    await redis.set(user_profile.tgid, json.dumps(profile.to_dict()))
                await api_chat_session_async.deactivate_generic_in_session(session_profile.id)
            else:
                await generate_image_model(message, user_profile)
        except BadRequestError as error:
            logger.error(error)
            await api_chat_session_async.deactivate_generic_in_session(session_profile.id)
            await api_chat_session_async.delete_context_from_session(session_profile.id, user_profile)
            await message.answer(Messages.ERROR.value)
            if error.code == "context_length_exceeded":
                # logger.error("BadRequestError error | MAX CONTEXT")
                return {"status": "error", "code": "max_content", "result": "Превышен контекст"}

            # logger.error(f"BadRequestError error | {error}  {error.code}")
            await message.answer(Messages.ERROR.value)
            return {"status": "error", "code": error.code, "result": ""}

        except Exception as error:
            logger.error(error)
            await api_chat_session_async.deactivate_generic_in_session(session_profile.id)
            await api_chat_session_async.delete_context_from_session(session_profile.id, user_profile)
            await message.answer(Messages.ERROR.value)
            if error.code == "context_length_exceeded":
                # logger.error("BadRequestError error | MAX CONTEXT")
                return {"status": "error", "code": "max_content", "result": "Превышен контекст"}
            return {"status": "error", "code": error.code, "result": ""}

# пример решения с помощью http

# url = 'https://api.openai.com/v1/chat/completions'
# headers = {
#     'Content-Type': 'application/json',
#     'Authorization': f'Bearer {settings.OPENAI_API_KEY}'
# }
# json_data = {
#     "model": "gpt-4o-mini",
#     "messages": [
#         {
#             "role": "system",
#             "content": "You are a helpful assistant."
#         },
#         {
#             "role": "user",
#             "content": message.text
#         }
#     ]
# }
# async with httpx.AsyncClient() as client:
#     response = await client.post(url, headers=headers, json=json_data)
#     content = json.loads(response.content)
#     await message.answer(content["choices"][0]["message"]["content"])