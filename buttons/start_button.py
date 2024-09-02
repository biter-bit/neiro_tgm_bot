from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.enum import MainButton, AiModel
from utils.models import Profile


def change_name_button(model: AiModel, profile: Profile) -> str:
    """Верни имя кнопки в нужном формате"""
    return f'✅ {model.code}' if profile.ai_model_id == model.code else model.code


async def gen_main_kb(user_profile, ai_models) -> ReplyKeyboardMarkup:
    """Верни основную клавиатуру бота телеграм"""
    button_start = KeyboardButton(text=MainButton.START.value)
    button_mj = KeyboardButton(text=change_name_button(ai_models[AiModel.MIDJORNEY.value], user_profile))
    button_gpt_3 = KeyboardButton(text=change_name_button(ai_models[AiModel.GPT_3_TURBO.value], user_profile))
    button_gpt_4 = KeyboardButton(text=change_name_button(ai_models[AiModel.GPT_4.value], user_profile))
    button_kandinsky = KeyboardButton(text=change_name_button(ai_models[AiModel.KANDINSKY.value], user_profile))
    builder = ReplyKeyboardMarkup(keyboard=[
        [button_mj, button_kandinsky],
        [button_gpt_3, button_gpt_4],
        [button_start],
    ], resize_keyboard=True)
    return builder
