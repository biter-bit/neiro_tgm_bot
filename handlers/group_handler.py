from aiogram import Router, types
from aiogram.filters import Command

ask_router = Router()

@ask_router.message(Command("ask"))
async def generate_text_in_group(message: types.Message):
    """Обработай генерацию в группе"""
    await message.answer("Запущен ask")