from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, Update
from services import logger
from typing import Any, Awaitable, Callable, Dict, Optional

class ExceptionMiddleware(BaseMiddleware):
    """
    Представляет обработчик всех необработанных исключений.
    """
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery | Update,
        data: Dict[str, Any],
    ) -> Any:
        """Обработай необработанные исключения."""
        try:
            return await handler(event, data)
        except Exception as e:
            logger.error(f"Пользователь {event.event.from_user.id}. Произошло необработанное исключение: {e}")
            if isinstance(event, Message):
                await event.answer("Произошла ошибка, пожалуйста, попробуйте еще раз.")
            elif isinstance(event, CallbackQuery):
                await event.message.answer("Произошла ошибка, пожалуйста, попробуйте еще раз.")
            elif isinstance(event, Update):
                await event.message.answer("Произошла ошибка, пожалуйста, попробуйте еще раз.")