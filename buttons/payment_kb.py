from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.callbacks import PaymentCallback
from utils.enum import PaymentName

async def gen_pay_inline_kb() -> InlineKeyboardMarkup:
    """Создай инлайн клавиатуру для оплаты подписки"""
    button_pay_stars = InlineKeyboardButton(
        text="Оплата Stars ⭐️",
        callback_data=PaymentCallback(option=PaymentName.STARS).pack()
    )
    button_pay_robokassa = InlineKeyboardButton(
        text="Оплата Robokassa 💵",
        callback_data=PaymentCallback(option=PaymentName.ROBOKASSA).pack()
    )
    builder = InlineKeyboardMarkup(inline_keyboard=[
        [button_pay_stars],
        [button_pay_robokassa],
    ])
    return builder