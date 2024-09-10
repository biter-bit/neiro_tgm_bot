from aiogram import Router, types
from aiogram.filters import Command
from utils.models import Profile
from utils.enum import Messages
from utils.db_api import get_all_ai_models
from buttons.main_kb import gen_main_kb

info_profile_router = Router()

@info_profile_router.message(Command("profile"))
async def cmd_get_info_profile(message: types.Message, user_profile: Profile):
    message_for_user = Messages.create_message_profile(user_profile)
    ai_models = await get_all_ai_models()
    markup = await gen_main_kb(user_profile, ai_models)
    await message.answer(message_for_user, reply_markup=markup)