from aiogram import types, enums
from aiogram import BaseMiddleware
from typing import Any, Awaitable, Callable, Dict
from aiogram.types import Message, CallbackQuery, TelegramObject

class RedirectGroupMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, types.Message):
            # Проверяем, является ли чат группой или каналом
            if event.chat.type != enums.ChatType.PRIVATE and not event.text.startswith('/ask'):
                # Вызываем обработчик для группового чата
                return await self.generate_text_in_group(event, data)

        # Если не группа, продолжаем с обычным обработчиком
        return await handler(event, data)


    async def generate_text_in_group(self, event: types.Message, data: Dict[str, Any]) -> Any:
        # Логика обработки сообщений из групп
        await event.answer("Эта команда работает только в режиме личных сообщений.")