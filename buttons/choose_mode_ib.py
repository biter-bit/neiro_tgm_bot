from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.enum import NameButtons, AiModelName
from db_api.models import Profile
from utils.callbacks import ModeCallback


def change_name_button(model: str, profile: Profile) -> str:
    """Верни имя кнопки в нужном формате"""
    return f'✅ {model}' if profile.ai_model_id == model else model


async def gen_choose_mode_kb(ai_models, profile) -> InlineKeyboardMarkup:
    """Верни основную клавиатуру бота телеграм"""

    builder = InlineKeyboardBuilder()

    for action in ai_models:
        builder.button(
            text=change_name_button(action, profile),
            callback_data=ModeCallback(action=change_name_button(model=action, profile=profile)),
        )

    builder.adjust(2, 2)

    return builder.as_markup()