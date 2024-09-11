from aiogram import Router
from aiogram.types import Message
from utils.models import Profile
from utils.enum import AiModelName
from utils.db_api import (
    get_or_create_session, create_text_query, get_text_messages_from_session, save_message, active_generic_in_session,
    deactivate_generic_in_session, delete_context_from_session, subtracting_tokens_from_profile_balance,
    subtracting_count_request_to_model_chatgpt_4o_mini
)
from services import chat_gpt
from openai import BadRequestError
from .image_model_handler import generate_image_model
from utils.features import check_limits_for_free_tariff, check_balance_profile

text_router = Router()

text_models_openai = [
    AiModelName.GPT_4_O_MINI.value, AiModelName.GPT_4_O.value
]

@text_router.message()
async def generate_text_model(message: Message, user_profile: Profile):
    """Обработай текстовые сообщения пользователей, которые являются prompt для текстовых нейронок"""
    session_profile = await get_or_create_session(user_profile, user_profile.ai_model_id)
    if session_profile.active_generation:
        return await message.answer('Генерация активна')

    current_model = user_profile.ai_model_id

    if user_profile.tariffs.name == "Free":
        if user_profile.ai_model_id == "gpt-4o":
            return await message.answer("Для доступа к этой модели поменяйте тариф!")
        if not check_limits_for_free_tariff(user_profile):
            return await message.answer("Вы превысили лимит запросов в сутки для этой модели!")
    else:
        if not check_balance_profile(user_profile):
            return await message.answer("Пополните баланс токенов!")

    try:
        if current_model in text_models_openai:
            await active_generic_in_session(session_profile.id)
            text_query = await create_text_query(message.text, session_profile.id)
            text_messages = await get_text_messages_from_session(session_profile.id, current_model)
            response = await chat_gpt.async_generate_text(
                ai_model=current_model, context=text_messages, prompt=message.text
            )
            await save_message(response.choices[0].message.content, text_query.id)
            await message.answer(f"{response.choices[0].message.content}")
            if user_profile.tariffs.name == "Free":
                await subtracting_count_request_to_model_chatgpt_4o_mini(user_profile.id)
            else:
                await subtracting_tokens_from_profile_balance(user_profile.id, user_profile.ai_models_id.cost)
            await deactivate_generic_in_session(session_profile.id)
        else:
            await generate_image_model(message, user_profile)
    except BadRequestError as error:
        await deactivate_generic_in_session(session_profile.id)
        await delete_context_from_session(session_profile.id, user_profile)
        if error.code == "context_length_exceeded":
            # logger.error("BadRequestError error | MAX CONTEXT")
            return {"status": "error", "code": "max_content", "result": "Превышен контекст"}

        # logger.error(f"BadRequestError error | {error}  {error.code}")
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