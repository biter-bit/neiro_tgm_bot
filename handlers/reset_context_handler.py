from aiogram.filters import Command
from aiogram import types, Router

from buttons.main_kb import gen_main_kb
from utils.enum import MainButton, Messages

from utils.db_api import async_session_db, get_all_ai_models, get_or_create_session, delete_context_from_session
from utils.models import Profile

from sqlalchemy.future import select

reset_router = Router()


@reset_router.message(Command("reset"))
async def reset_context(message: types.Message, user_profile: Profile):
    """Обработай запрос при команде /reset"""
    commands = Messages.RESET.value
    ai_models = await get_all_ai_models()
    markup = await gen_main_kb(user_profile, ai_models)
    session_obj = await get_or_create_session(user_profile, user_profile.ai_model_id)
    await delete_context_from_session(session_obj.id, user_profile)
    await message.answer(commands, reply_markup=markup)