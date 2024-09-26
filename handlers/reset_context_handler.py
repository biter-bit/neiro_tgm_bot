from aiogram.filters import Command
from aiogram import types, Router

from utils.enum import Messages

from db_api import api_chat_session_async
from db_api.models import Profile

reset_router = Router()


@reset_router.message(Command("reset"))
async def reset_context(message: types.Message, user_profile: Profile):
    """Обработай запрос при команде /reset"""
    session_obj = await api_chat_session_async.get_or_create_session(user_profile, user_profile.ai_model_id)
    await api_chat_session_async.delete_context_from_session(session_obj.id, user_profile)
    await message.answer(Messages.RESET.value)