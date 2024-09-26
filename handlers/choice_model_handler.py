from aiogram import Router
from aiogram import types
from aiogram.filters import Command
from buttons.choose_mode_ib import gen_choose_mode_kb
from utils.enum import AiModelName, Messages
from db_api import api_profile_async, api_ai_model_async, db_api_async_obj
from db_api.models import Profile, ChatSession
from buttons.main_kb import gen_main_kb
from aiogram.fsm.context import FSMContext
from states.type_generation import TypeState
from buttons.choose_mode_ib import gen_choose_mode_kb
from utils.callbacks import ModeCallback

choice_model_router = Router()


@choice_model_router.message(Command("mode"))
async def choice_mode(message: types.Message, user_profile: Profile):
    """Обработай запрос пользователя на получение подписки"""
    commands = Messages.CHOICE_MODE.value
    ai_models = await api_ai_model_async.get_all_ai_models()
    kb_inline = await gen_choose_mode_kb(ai_models, user_profile)
    await message.answer(commands, reply_markup=kb_inline)

@choice_model_router.callback_query(ModeCallback.filter())
async def choice_ai_model_for_profile(query: types.CallbackQuery, callback_data: ModeCallback, user_profile: Profile, state: FSMContext,
                                      session_profile: ChatSession):
    """Поменяй активную модель пользователя"""

    model_without_check_mark = callback_data.action.replace('✅ ', '')
    profile_obj = await api_profile_async.replace_model_of_profile(user_profile, model_without_check_mark)

    ai_models = await api_ai_model_async.get_all_ai_models()
    markup = await gen_choose_mode_kb(ai_models, profile_obj)
    session_profile.ai_model_id = profile_obj.ai_model_id
    await db_api_async_obj.update_data(session_profile)
    if profile_obj.ai_models_id.type == "text":
        await state.set_state(TypeState.text)
    else:
        await state.set_state(TypeState.image)
    await query.message.edit_reply_markup(reply_markup=markup)