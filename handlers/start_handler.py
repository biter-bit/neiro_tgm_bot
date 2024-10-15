from aiogram.filters import CommandStart
from aiogram import types, Router
from utils.enum import Messages
from aiogram.types import ReplyKeyboardRemove
from services import logger
from db_api import api_ref_link_async
from config import settings
from aiogram.exceptions import TelegramForbiddenError

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: types.Message):
    """Обработай запрос команды /start"""
    message_start = Messages.START.value
    try:
        await message.answer(message_start, reply_markup=ReplyKeyboardRemove())
    except TelegramForbiddenError:
        logger.error(f"Бот был удален у пользователя {message.from_user.id}")