from aiogram import types, enums
from aiogram.filters import Command
from handlers.text_model_handler import generate_text_model, handle_photo
from aiogram import Router
from utils.enum import AiModelName
from db_api.models import Profile
from aiogram.types import ContentType
from aiogram import F

ask_router = Router()

@ask_router.message(Command("ask"))
async def generate_text_in_group(message: types.Message, user_profile: Profile):
    """Обработай генерацию в группе"""
    if message.chat.type != enums.ChatType.PRIVATE:
        if F.content_type == ContentType.PHOTO:
            await generate_text_model(message, user_profile)
        else:
            await handle_photo(message, user_profile)
    else:
        await message.answer("Эта команда работает только в группах.")