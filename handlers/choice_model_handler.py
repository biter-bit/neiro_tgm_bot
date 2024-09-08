from aiogram import Router
from aiogram import types
from utils.enum import AiModelName, Messages
from utils.db_api import async_session_db, get_all_ai_models
from utils.models import Profile
from sqlalchemy import select
from buttons.start_button import gen_main_kb

choice_model_router = Router()


@choice_model_router.message(lambda message: message.text in [model.value for model in AiModelName] + [f'✅ {model.value}' for model in AiModelName])
async def handle_ai_model(message: types.Message, user_profile: str):
    """Обработай callback пользователя при нажатии на модель нейронки"""

    ai_models = await get_all_ai_models()
    async with async_session_db() as session:
        stmt = select(Profile).filter_by(tgid=user_profile.tgid)
        profile = await session.execute(stmt)
        profile = profile.scalars().first()
        profile.ai_model_id = message.text.replace('✅ ', '')
        await session.commit()
        await session.refresh(profile)
    markup = await gen_main_kb(profile, ai_models)
    await message.answer(Messages.START.value, reply_markup=markup)