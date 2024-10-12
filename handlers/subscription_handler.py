from aiogram.filters import Command
from aiogram.types import LabeledPrice, PreCheckoutQuery, ContentType, Message
from aiogram import types, Router, F

from buttons.payment_kb import gen_pay_inline_kb, gen_confirm_pay_kb
from config import settings
from utils.enum import Messages, PaymentName, Price
from utils.callbacks import PaymentCallback
from db_api import api_invoice_async, api_profile_async, api_tariff_async
from services import robokassa_obj
import json
from utils.cache import set_cache_profile

from db_api.models import Profile

pay_router = Router()

@pay_router.message(Command("pay"))
async def subscription_pay(message: types.Message, user_profile: Profile):
    """Обработай запрос пользователя на получение подписки (команда /pay)"""
    if user_profile.tariff_id == 2:
        await message.answer("Ваш тариф 'Plus' уже активирован")
        return
    commands = Messages.PAY.value
    kb_inline = await gen_pay_inline_kb()
    await message.answer(commands, reply_markup=kb_inline)

@pay_router.callback_query(PaymentCallback.filter(F.option == PaymentName.STARS))
async def payment_stars_handler(callback: types.CallbackQuery, user_profile: Profile):
    """Обработай оплату с помощью звезд telegram."""
    tariff = await api_tariff_async.get_tariff(2)
    is_mother = True
    invoice_mother = await api_invoice_async.get_invoice_mother(user_profile.id)
    if invoice_mother:
        is_mother = False
    invoice = await api_invoice_async.create_invoice(
        profile_id=user_profile.id, tariff_id=tariff.id, provider=PaymentName.STARS, is_mother=is_mother
    )
    description = f"Оплата подписки PREMIUM {tariff.price_stars}"
    await callback.message.answer_invoice(
        title=description,
        description=description,
        currency="XTR",
        prices=[LabeledPrice(label=description, amount=1)],
        payload=str(invoice.id),
        provider_token="",
    )
    # await callback.answer()

@pay_router.pre_checkout_query()
async def pre_checkout_handler(query: PreCheckoutQuery):
    """Выполни действие перед оплатой звездами"""
    await query.answer(ok=True)

@pay_router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def success_payment_handler(message: Message, user_profile: Profile):
    """Выполни действие после оплаты звездами"""
    inv_id = int(message.successful_payment.invoice_payload)
    invoice = await api_invoice_async.pay_invoice(inv_id)
    profile = await api_profile_async.update_subscription_profile(invoice.profiles.id, invoice.tariffs.id)
    await set_cache_profile(profile.tgid, json.dumps(profile.to_dict()))
    await message.bot.refund_star_payment(message.from_user.id, message.successful_payment.telegram_payment_charge_id)
    await message.answer(text="Success")

@pay_router.callback_query(PaymentCallback.filter(F.option == PaymentName.ROBOKASSA))
async def payment_robokassa_handler(callback: types.CallbackQuery, user_profile: Profile):
    """Обработай оплату с помощью карты (rub)"""
    tariff = await api_tariff_async.get_tariff(2)
    is_mother = True
    invoice_mother = await api_invoice_async.get_invoice_mother(user_profile.id)
    if invoice_mother:
        is_mother = False
    invoice = await api_invoice_async.create_invoice(
        profile_id=user_profile.id, tariff_id=tariff.id, provider=PaymentName.ROBOKASSA, is_mother=is_mother
    )
    description = f"Оплата подписки PREMIUM {tariff.price_rub}"
    redirect_url = robokassa_obj.gen_pay_url(
        user_id=user_profile.id, inv_id=invoice.id, tariff_desc=tariff.name, price=Price.RUB.value,
        recurring=settings.RECURRING
    )
    markup = await gen_confirm_pay_kb(tariff=tariff, redirect_url=redirect_url)
    await callback.message.answer(text=description, reply_markup=markup, disable_web_page_preview=True)
