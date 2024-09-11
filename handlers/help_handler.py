from aiogram.filters import Command
from aiogram import types, Router

from utils.enum import Messages

from utils.db_api import get_or_create_session
from utils.models import Profile

help_router = Router()

@help_router.message(Command("help"))
async def get_info_help(message: types.Message, user_profile: Profile):
    """Обработай запрос команды /help"""
    await get_or_create_session(user_profile, user_profile.ai_model_id)
    await message.answer(Messages.HELP.value)