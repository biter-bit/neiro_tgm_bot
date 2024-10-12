from aiogram import Router
from aiogram import types
from aiogram.filters import Command
from utils.features import get_session_for_profile
from utils.enum import Messages
from db_api import api_profile_async, api_ai_model_async, db_api_async_obj
from db_api.models import Profile
from aiogram.fsm.context import FSMContext
from states.type_generation import TypeAiState
from buttons.choose_mode_ib import gen_choose_mode_kb
from utils.callbacks import ModeCallback
from aiogram.exceptions import TelegramBadRequest
from services import logger
from utils.cache import set_cache_profile, serialization_profile

choice_model_router = Router()


@choice_model_router.message(Command("mode"))
async def choice_mode(message: types.Message, user_profile: Profile):
    """Обработай запрос пользователя на получение подписки"""
    commands = Messages.CHOICE_MODE.value
    ai_models = await api_ai_model_async.get_all_ai_models()
    kb_inline = await gen_choose_mode_kb(ai_models, user_profile)
    await message.answer(commands, reply_markup=kb_inline)

@choice_model_router.callback_query(ModeCallback.filter())
async def choice_ai_model_for_profile(query: types.CallbackQuery, callback_data: ModeCallback, user_profile: Profile, state: FSMContext):
    """Поменяй активную модель пользователя"""
    session_profile = await get_session_for_profile(user_profile, callback_data.action)
    model_without_check_mark = callback_data.action.replace('✅ ', '')
    profile_obj = await api_profile_async.replace_model_of_profile(user_profile, model_without_check_mark)
    await set_cache_profile(profile_obj.tgid, await serialization_profile(profile_obj))

    ai_models = await api_ai_model_async.get_all_ai_models()
    markup = await gen_choose_mode_kb(ai_models, profile_obj)
    session_profile.ai_model_id = profile_obj.ai_model_id
    await db_api_async_obj.update_data(session_profile)
    if profile_obj.ai_models_id.type == "text":
        await state.set_state(TypeAiState.text)
    else:
        await state.set_state(TypeAiState.image)
    try:
        await query.message.edit_reply_markup(reply_markup=markup)
    except TelegramBadRequest as e:
        logger.info(e)