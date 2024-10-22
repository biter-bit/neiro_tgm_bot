from aiogram.filters import CommandStart
from aiogram import types, Router
from utils.enum import Messages, MainButtons
from aiogram.types import ReplyKeyboardRemove
from services import logger
from aiogram.exceptions import TelegramForbiddenError

start_router = Router()

@start_router.message(lambda message: message.text == "/start" or message.text in [btn.value for btn in MainButtons])
async def cmd_start(message: types.Message):
    """Обработай запрос команды /start"""
    message_start = Messages.START.value
    try:
        await message.answer(message_start, reply_markup=ReplyKeyboardRemove())
    except TelegramForbiddenError:
        logger.error(f"Бот был удален у пользователя {message.from_user.id}")