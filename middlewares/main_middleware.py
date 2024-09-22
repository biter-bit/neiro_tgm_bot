from aiogram import BaseMiddleware
from typing import Any, Awaitable, Callable, Dict
from aiogram.enums import ChatMemberStatus
from aiogram.types import Message, CallbackQuery, TelegramObject, InlineKeyboardButton, InlineKeyboardMarkup
from tgbot_app.db_api.models import Profile
from db_api import api_profile_async, api_chat_session_async
from utils.enum import AiModelName, TariffCode, NameButtons
from config import settings

class MainMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:

        command = data.get("command")
        user_profile: Profile = data["user_profile"]

        if isinstance(event, Message) and event.text:
            if event.text in AiModelName.get_list_value() or event.text in NameButtons.get_list_value() or event.text.startswith('/'):
                return await handler(event, data)

        if user_profile.is_staff or user_profile.tariffs.code.value != TariffCode.FREE.value:
            return await handler(event, data)

        status_1 = await event.bot.get_chat_member(chat_id=settings.CHANNELS_IDS[0], user_id=event.from_user.id)
        # status_2 = await event.bot.get_chat_member(chat_id=settings.CHANNELS_IDS[1], user_id=event.from_user.id)

        if user_profile.count_request == 3 and status_1.status in (ChatMemberStatus.LEFT, ChatMemberStatus.KICKED):
            text = "Чтобы пользоваться самым лучшим ботом необходимо подписаться на наш канал!"
            markup = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Подписаться", url=f"https://t.me/{settings.CHANNELS_NAMES[0]}")]
                ]
            )

        # elif status_2.status in (ChatStatus.LEFT, ChatStatus.KICKED):
        #     text = "Чтобы продолжить пользоваться самым лучшим ботом необходимо подписаться на наш второй канал!"
        #     markup = InlineKeyboardMarkup(
        #         inline_keyboard=[
        #             [InlineKeyboardButton(text="Подписаться", url=f"https://t.me/{settings.CHANNELS_NAMES[1]}")]
        #         ]
        #     )
        else:
            return await handler(event, data)

        if isinstance(event, CallbackQuery):
            await event.message.answer(text=text, reply_markup=markup, disable_web_page_preview=True)
            await event.answer()
        else:
            await event.answer(text=text, reply_markup=markup, disable_web_page_preview=True)