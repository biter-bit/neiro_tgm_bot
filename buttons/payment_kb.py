from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from utils.enum import MainButton, AiModelName
from utils.models import Profile

async def gen_pay_inline_kb() -> InlineKeyboardMarkup:
    """Создай инлайн клавиатуру для оплаты подписки"""
    button_pay_stars = InlineKeyboardButton(text="Оплата Stars ⭐️", callback_data='inline_btn1')
    button_pay_robokassa = InlineKeyboardButton(text="Оплата Robokassa 💵", callback_data='inline_btn2')
    builder = InlineKeyboardMarkup(inline_keyboard=[
        [button_pay_stars],
        [button_pay_robokassa],
    ])
    return builder