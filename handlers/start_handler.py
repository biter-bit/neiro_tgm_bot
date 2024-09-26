from aiogram.filters import Command
from aiogram import types, Router

from buttons.main_kb import gen_main_kb
from utils.enum import NameButtons, Messages

from db_api import api_ai_model_async
from db_api.models import Profile
from aiogram.fsm.context import FSMContext
from states.type_generation import TypeState
from aiogram.types import ReplyKeyboardRemove

from sqlalchemy.future import select

start_router = Router()


@start_router.message(Command("start"))
@start_router.message(lambda message: message.text == NameButtons.START.value)
async def cmd_start(message: types.Message, user_profile: Profile, state: FSMContext):
    """Обработай запрос при нажатии кнопки 'Перезапуск бота' и текста 'start'"""
    commands = Messages.START.value
    await state.set_state(TypeState.text)
    await message.answer(commands, reply_markup=ReplyKeyboardRemove())