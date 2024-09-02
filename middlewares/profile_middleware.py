from aiogram import BaseMiddleware
from typing import Any, Awaitable, Callable, Dict
from aiogram.types import Message
from utils.db_api import get_or_create_profile


class ProfileMiddleware(BaseMiddleware):
    """Представляет из себя класс по работе с пользователем, который выполняется до и после обработчика"""
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        """Создай пользователя, если его нет в базе данных"""
        user = event.event.from_user
        profile = await get_or_create_profile(
            tgid=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            url=user.url
        )

        data['user_profile'] = profile

        return await handler(event, data)