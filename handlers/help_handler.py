from aiogram.filters import Command
from aiogram import types, Router

from buttons.main_kb import gen_main_kb
from utils.enum import MainButton, Messages

from utils.db_api import async_session_db, get_all_ai_models, get_or_create_session
from utils.models import Profile

from sqlalchemy.future import select

help_router = Router()


@help_router.message(Command("help"))
async def cmd_start(message: types.Message, user_profile: Profile):
    """Обработай запрос команды /help"""
    commands = Messages.HELP.value
    ai_models = await get_all_ai_models()
    markup = await gen_main_kb(user_profile, ai_models)
    await get_or_create_session(user_profile, user_profile.ai_model_id)
    await message.answer(commands, reply_markup=markup)