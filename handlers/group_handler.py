from aiogram import Router, types
from aiogram.filters import Command
from utils.models import Profile
from utils.enum import Messages

ask_router = Router()

@ask_router.message(Command("ask"))
async def generate_text_in_group(message: types.Message, user_profile: Profile):
    """Обработай генерацию в группе"""
    await message.answer("Запущен ask")