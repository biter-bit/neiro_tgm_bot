from aiogram import Router
from aiogram import types
from utils.enum import AiModel, Messages
from utils.db_api import async_session_db
from utils.models import Profile
from sqlalchemy import select
from buttons.start_button import gen_main_kb

choice_model_router = Router()


@choice_model_router.message(lambda message: message.text in [model.value for model in AiModel] + [f'✅ {model.value}' for model in AiModel])
async def handle_ai_model(message: types.Message, user_profile: str):
    result = AiModel.get_enum_field_by_value(message.text.replace('✅ ', ''))
    async with async_session_db() as session:
        stmt = select(Profile).filter_by(tgid=user_profile.tgid)
        profile = await session.execute(stmt)
        profile = profile.scalars().first()
        profile.model = result.name
        await session.commit()
        await session.refresh(profile)
    markup = await gen_main_kb(profile)
    await message.answer(Messages.START.value, reply_markup=markup)