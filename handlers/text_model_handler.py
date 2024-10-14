from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, ContentType

from db_api.models import Profile
from utils.enum import AiModelName, Messages
from db_api import api_chat_session_async, api_text_query_async, api_profile_async
from services import chat_gpt, logger, bot
from openai import BadRequestError
from .image_model_handler import generate_image_model
from utils.features import check_start_text_generate, get_session_for_profile
from utils.states import TypeAiState
import json
from io import BytesIO
import base64
from utils.cache import set_cache_profile

text_router = Router()

text_models_openai = [
    AiModelName.GPT_4_O_MINI.value, AiModelName.GPT_4_O.value, AiModelName.GPT_O1_MINI.value,
    AiModelName.GPT_O1_PREVIEW.value
]


async def handle_photo(message, session_profile, current_model):
    photo = message.photo[-1]  # Берем фото с максимальным разрешением
    file_info = await bot.get_file(photo.file_id)

    # Загружаем фото в байты
    file = await bot.download_file(file_info.file_path)

    # Читаем данные и кодируем в base64
    buffer = BytesIO(file.read())
    encoded_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

    message_dict = json.dumps({'type': 'text', 'text': message.md_text})
    photo_dict = json.dumps({'type': 'image_url', 'image_url': {"url": f"data:image/jpeg;base64,{encoded_image}"}})

    text_messages = await api_chat_session_async.get_text_messages_from_session(session_profile.id,
                                                                                current_model)
    deserialization_list = [json.loads(message_dict), json.loads(photo_dict)]
    response = await chat_gpt.async_generate_text(
        ai_model=current_model, context=text_messages, prompt=deserialization_list
    )
    await message.reply(f"{response.choices[0].message.content}")

@text_router.message(TypeAiState.text)
async def generate_text_model(message: Message, user_profile: Profile):
    """Обработай текстовые сообщения пользователей, которые являются prompt для текстовых нейронок"""
    session_profile = await get_session_for_profile(user_profile, user_profile.ai_model_id)
    if user_profile.ai_model_id in text_models_openai:

        the_check_failed = await check_start_text_generate(message, user_profile, session_profile)
        if the_check_failed['status']:
            await message.answer(the_check_failed['text'])
            return

        current_model = user_profile.ai_model_id

        if current_model not in text_models_openai:
            await generate_image_model(message, user_profile)
        else:
            await api_chat_session_async.active_generic_in_session(session_profile.id)
            if message.content_type == ContentType.PHOTO.value:
                if current_model == AiModelName.GPT_4_O.value:
                    await handle_photo(message, session_profile, current_model)
                else:
                    await message.answer(
                        "Похоже, что вы прикрепили изображение. Считывание изображений доступно в GPT-4o. "
                        "Выберите языковую модель по команде /mode"
                    )
                await api_chat_session_async.deactivate_generic_in_session(session_profile.id)
                return

            text_query = await api_text_query_async.create_text_query(message.text, session_profile.id)
            text_messages = await api_chat_session_async.get_text_messages_from_session(session_profile.id, current_model)

            try:
                response = await chat_gpt.async_generate_text(
                    ai_model=current_model, context=text_messages, prompt=message.text
                )
                text = response.choices[0].message.content

                await api_text_query_async.save_message(text, text_query.id)

                text_lst = [text[x:x + 4096] for x in range(0, len(text), 4096)] if len(text) > 4096 else [text]

                for part in text_lst:
                    if part:
                        try:
                            await message.answer(text=part)
                        except TelegramBadRequest:
                            await message.answer(text=part)

                if user_profile.ai_model_id == AiModelName.GPT_4_O.value and user_profile.chatgpt_4o_daily_limit > 0:
                    profile = await api_profile_async.subtracting_count_request_to_model_gpt(user_profile.id, user_profile.ai_model_id)
                    await set_cache_profile(user_profile.tgid, json.dumps(profile.to_dict()))
                await api_chat_session_async.deactivate_generic_in_session(session_profile.id)
            except BadRequestError as error:
                logger.error(error)
                await api_chat_session_async.deactivate_generic_in_session(session_profile.id)
                await api_chat_session_async.delete_context_from_session(session_profile.id, user_profile)
                await message.answer(Messages.ERROR.value)
                if error == "context_length_exceeded":
                    return {"status": "error", "code": "max_content", "result": "Превышен контекст"}
                await message.answer(Messages.ERROR.value)
                return {"status": "error", "code": error, "result": ""}

            except Exception as error:
                logger.error(error)
                await api_chat_session_async.deactivate_generic_in_session(session_profile.id)
                await api_chat_session_async.delete_context_from_session(session_profile.id, user_profile)
                await message.answer(Messages.ERROR.value)
                if error == "context_length_exceeded":
                    return {"status": "error", "code": "max_content", "result": "Превышен контекст"}
                return {"status": "error", "code": error, "result": ""}