from aiogram import Router
from aiogram import types
from utils.enum import AiModelName, Messages
from utils.db_api import get_all_ai_models, get_or_create_session, replace_model_of_profile
from utils.models import Profile
from buttons.main_kb import gen_main_kb
from aiogram.fsm.context import FSMContext
from states.type_generation import TypeState

choice_model_router = Router()


@choice_model_router.message(lambda message: message.text in [model.value for model in AiModelName] + [f'✅ {model.value}' for model in AiModelName])
async def choice_ai_model_for_profile(message: types.Message, user_profile: Profile, state: FSMContext):
    """Поменяй активную модель пользователя"""

    model_without_check_mark = message.text.replace('✅ ', '')
    profile_obj = await replace_model_of_profile(user_profile, model_without_check_mark)

    ai_models = await get_all_ai_models()
    markup = await gen_main_kb(profile_obj, ai_models)
    await get_or_create_session(profile_obj, profile_obj.ai_model_id)
    if profile_obj.ai_models_id.type == "text":
        await state.set_state(TypeState.text)
    else:
        await state.set_state(TypeState.image)
    await message.answer(Messages.create_message_choice_model(profile_obj.ai_model_id), reply_markup=markup)