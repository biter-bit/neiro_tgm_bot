from aiogram import Router
from aiogram.types import Message, InputFile, FSInputFile, BufferedInputFile, URLInputFile
from utils.models import Profile
from utils.enum import AiModelName
from utils.db_api import get_or_create_session, active_generic_in_session, deactivate_generic_in_session
from utils.features import check_balance_profile
from PIL import Image
from io import BytesIO
from services import nlp_translator, midjourney_obj

image_router = Router()

image_models = [
    AiModelName.MIDJORNEY.value,
]

@image_router.message()
async def generate_image_model(message: Message, user_profile: Profile):
    """Обработай текстовые сообщения пользователей, которые являются prompt для нейронок изображений"""
    session_profile = await get_or_create_session(user_profile, user_profile.ai_model_id)
    if session_profile.active_generation:
        return await message.answer('Генерация активна')

    current_model = user_profile.ai_model_id

    if user_profile.tariffs.name == "Free":
        return await message.answer("Для доступа к этой модели поменяйте тариф!")
    else:
        if not check_balance_profile(user_profile):
            return await message.answer("Пополните баланс токенов!")

    if current_model == AiModelName.MIDJORNEY.value:
        await active_generic_in_session(session_profile.id)
        content = await nlp_translator.async_translate(text=message.text)
        result = await midjourney_obj.async_generate_image(content['result'])
        if result['status'] == 'failed':
            await message.answer("Попробуйте сделать запрос снова")
        elif result['status'] == 'completed':
            await message.answer_photo(
                URLInputFile(result['attachments'][0]['url']),
                caption='Вот изображение!'
            )
        await deactivate_generic_in_session(session_profile.id)