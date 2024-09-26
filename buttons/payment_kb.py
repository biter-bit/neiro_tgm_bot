from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from utils.callbacks import PaymentCallback
from utils.enum import PaymentName
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db_api.models import Profile, Tariff

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

async def gen_confirm_pay_kb(tariff: Tariff, redirect_url: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=f"Оплатить {tariff.price_rub}р.", web_app=WebAppInfo(url=redirect_url))

    return builder.as_markup()