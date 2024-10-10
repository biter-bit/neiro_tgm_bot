from aiogram.filters import Command
from aiogram.types import LabeledPrice, PreCheckoutQuery, ContentType, Message
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from buttons.payment_kb import gen_pay_inline_kb, gen_confirm_pay_kb
from utils.enum import Messages, PaymentName
from utils.callbacks import PaymentCallback
from db_api import api_invoice_async, api_profile_async, api_tariff_async
from services import robokassa_obj, redis
import json

from db_api.models import Profile, Invoice

pay_router = Router()


@pay_router.message(Command("pay"))
async def subscription_pay(message: types.Message, user_profile: Profile):
    """Обработай запрос пользователя на получение подписки"""
    if user_profile.tariff_id == 2:
        await message.answer("Ваш тариф 'Plus' уже активирован")
        return
    commands = Messages.PAY.value
    kb_inline = await gen_pay_inline_kb()
    await message.answer(commands, reply_markup=kb_inline)

@pay_router.callback_query(PaymentCallback.filter(F.option == PaymentName.STARS))
async def payment_stars_handler(callback: types.CallbackQuery, user_profile: Profile, callback_data: PaymentCallback):
    tariff = await api_tariff_async.get_tariff(2)
    invoice = await api_invoice_async.create_invoice(
        profile_id=user_profile.id, tariff_id=tariff.id, provider=PaymentName.STARS
    )
    description = f"Оплата подписки PREMIUM {tariff.price_stars}"
    await callback.message.answer_invoice(
        title=description,
        description=description,
        currency="XTR",
        prices=[LabeledPrice(label=description, amount=190)],
        payload=str(invoice.id),
        provider_token="",
    )
    await callback.answer()

@pay_router.callback_query(PaymentCallback.filter(F.option == PaymentName.ROBOKASSA))
async def payment_robokassa_handler(callback: types.CallbackQuery, user_profile: Profile, callback_data: PaymentCallback):
    tariff = await api_tariff_async.get_tariff(2)
    invoice = await api_invoice_async.create_invoice(
        profile_id=user_profile.id, tariff_id=tariff.id, provider=PaymentName.STARS
    )
    description = f"Оплата подписки PREMIUM {tariff.price_rub}"
    redirect_url = robokassa_obj.gen_pay_url(
        user_id=user_profile.id, inv_id=invoice.id, tariff_desc=tariff.name, price=489, recurring=True
    )
    markup = await gen_confirm_pay_kb(tariff=tariff, redirect_url=redirect_url)
    await callback.message.answer(text=description, reply_markup=markup, disable_web_page_preview=True)

@pay_router.pre_checkout_query()
async def pre_checkout_handler(query: PreCheckoutQuery):
    inv_id = int(query.invoice_payload)
    invoice = await api_invoice_async.pay_invoice(inv_id)
    profile = await api_profile_async.update_subscription_profile(invoice.profiles.id, invoice.tariffs.id)
    await redis.set(profile.tgid, json.dumps(profile.to_dict()))
    await query.answer(ok=True)

@pay_router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def success_payment_handler(message: Message, user_profile: Profile, state: FSMContext):
    # await message.bot.refund_star_payment(message.from_user.id, message.successful_payment.telegram_payment_charge_id)
    await profile_info(message=message)

async def profile_info(message: Message):
    await message.answer(text="Success")

# @pay_router.message(Command(MainCommands.TARIFFS.command))
# @pay_router.message(F.text == MainButtons.PROFILE.value)
# async def profile_info(message: Message, profile: Profile, state: FSMContext):
#     await state.clear()
#
#     text = await gen_profile_text(profile)
#     markup = await gen_profile_kb(profile)
#
#     await message.answer(text=text, reply_markup=markup)
