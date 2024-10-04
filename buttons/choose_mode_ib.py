from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.enum import NameButtons, AiModelName
from db_api.models import Profile
from utils.callbacks import ModeCallback


def change_name_button(model: str, profile: Profile) -> str:
    """Верни имя кнопки в нужном формате"""
    return f'✅ {AiModelName.get_need_format(model)}' if profile.ai_model_id == model else AiModelName.get_need_format(model)


async def gen_choose_mode_kb(ai_models, profile) -> InlineKeyboardMarkup:
    """Верни основную клавиатуру бота телеграм"""

    builder = InlineKeyboardBuilder()

    for model in ai_models:
        builder.button(
            text=change_name_button(model, profile),
            callback_data=ModeCallback(action=model),
        )

    builder.adjust(2, 2)

    return builder.as_markup()