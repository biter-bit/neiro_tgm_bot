from aiogram.filters import Command
from aiogram import types, Router

from utils.enum import Messages

from utils.db_api import get_or_create_session, delete_context_from_session
from utils.models import Profile

reset_router = Router()


@reset_router.message(Command("reset"))
async def reset_context(message: types.Message, user_profile: Profile):
    """Обработай запрос при команде /reset"""
    session_obj = await get_or_create_session(user_profile, user_profile.ai_model_id)
    await delete_context_from_session(session_obj.id, user_profile)
    await message.answer(Messages.RESET.value)