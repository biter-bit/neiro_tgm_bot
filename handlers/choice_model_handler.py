from aiogram import Router
from aiogram import types
from utils.enum import AiModelName, Messages
from db_api import api_profile_async, api_ai_model_async, db_api_async_obj
from tgbot_app.db_api.models import Profile, ChatSession
from buttons.main_kb import gen_main_kb
from aiogram.fsm.context import FSMContext
from states.type_generation import TypeState

choice_model_router = Router()


@choice_model_router.message(lambda message: message.text in [model.value for model in AiModelName] + [f'✅ {model.value}' for model in AiModelName])
async def choice_ai_model_for_profile(message: types.Message, user_profile: Profile, state: FSMContext,
                                      session_profile: ChatSession):
    """Поменяй активную модель пользователя"""

    model_without_check_mark = message.text.replace('✅ ', '')
    profile_obj = await api_profile_async.replace_model_of_profile(user_profile, model_without_check_mark)

    ai_models = await api_ai_model_async.get_all_ai_models()
    markup = await gen_main_kb(profile_obj, ai_models)
    session_profile.ai_model_id = profile_obj.ai_model_id
    await db_api_async_obj.update_data(session_profile)
    if profile_obj.ai_models_id.type == "text":
        await state.set_state(TypeState.text)
    else:
        await state.set_state(TypeState.image)
    await message.answer(Messages.create_message_choice_model(profile_obj.ai_model_id), reply_markup=markup)