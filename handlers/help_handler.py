from aiogram.filters import Command
from aiogram import types, Router

from utils.enum import Messages


help_router = Router()

@help_router.message(Command("help"))
async def get_info_help(message: types.Message):
    """Обработай запрос команды /help"""
    await message.answer(Messages.HELP.value)