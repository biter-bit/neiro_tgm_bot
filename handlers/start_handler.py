from aiogram.filters import CommandStart
from aiogram import types, Router
from utils.enum import Messages
from aiogram.types import ReplyKeyboardRemove
from services import logger
from db_api import api_ref_link_async
from config import settings

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: types.Message):
    """Обработай запрос команды /start"""
    list_arg = message.text.split(' ')
    if len(list_arg) == 2:
        try:
            num_link = int(list_arg[1])
            await api_ref_link_async.add_click(f'{settings.USERNAME_BOT}?start={num_link}')
        except TypeError as e:
            logger.error("Команда /start с данным аргументом не работает")

    message_start = Messages.START.value
    await message.answer(message_start, reply_markup=ReplyKeyboardRemove())