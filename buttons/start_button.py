from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.enum import MainButton, AiModel
from utils.models import Profile


def change_name_button(model: AiModel, profile: Profile) -> str:
    """Верни имя кнопки в нужном формате"""
    return f'✅ {model.value}' if profile.model == model else model.value


async def gen_main_kb(user_profile) -> ReplyKeyboardMarkup:
    """Верни основную клавиатуру бота телеграм"""
    button_start = KeyboardButton(text=MainButton.START.value)
    button_mj = KeyboardButton(text=change_name_button(AiModel.MIDJORNEY, user_profile))
    button_gpt_3 = KeyboardButton(text=change_name_button(AiModel.GPT_3_TURBO, user_profile))
    button_gpt_4 = KeyboardButton(text=change_name_button(AiModel.GPT_4, user_profile))
    button_kandinsky = KeyboardButton(text=change_name_button(AiModel.KANDINSKY, user_profile))
    builder = ReplyKeyboardMarkup(keyboard=[
        [button_mj, button_kandinsky],
        [button_gpt_3, button_gpt_4],
        [button_start],
    ], resize_keyboard=True)
    return builder
