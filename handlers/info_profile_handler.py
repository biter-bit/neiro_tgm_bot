from aiogram import Router, types
from aiogram.filters import Command
from utils.models import Profile
from utils.enum import Messages

info_profile_router = Router()

@info_profile_router.message(Command("profile"))
async def get_info_profile(message: types.Message, user_profile: Profile):
    message_for_user = Messages.create_message_profile(user_profile)
    await message.answer(message_for_user)