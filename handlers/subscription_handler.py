from aiogram.filters import Command
from aiogram import types, Router, F

from buttons.payment_kb import gen_pay_inline_kb
from utils.enum import MainButton, Messages

from utils.db_api import async_session_db, get_all_ai_models, get_or_create_session
from utils.models import Profile

pay_router = Router()


@pay_router.message(Command("pay"))
async def subscription_pay(message: types.Message, user_profile: Profile):
    """Обработай запрос пользователя на получение подписки"""
    commands = Messages.PAY.value
    kb_inline = await gen_pay_inline_kb()
    await get_or_create_session(user_profile, user_profile.ai_model_id)
    await message.answer(commands, reply_markup=kb_inline)

@pay_router.callback_query(F.data == 'inline_btn1')
async def payment_stars_handler(callback: types.CallbackQuery, user_profile: Profile):
    await callback.message.answer('hello')