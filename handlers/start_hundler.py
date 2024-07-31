from aiogram.filters import Command
from aiogram import types, Router

from buttons.start_button import gen_main_kb
from utils.enum import MainButton, Messages

from utils.db_api import async_session_db
from utils.models import Profile

from sqlalchemy.future import select

start_router = Router()


@start_router.message(Command("start"))
@start_router.message(lambda message: message.text == MainButton.START.value)
async def cmd_start(message: types.Message, counter: str, user_profile: str):
    """Обработай запрос при нажатии кнопки 'Перезапуск бота' и текста 'start'"""
    commands = Messages.START.value
    markup = await gen_main_kb(user_profile)
    await message.answer(commands, reply_markup=markup)