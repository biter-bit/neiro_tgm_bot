from aiogram import BaseMiddleware
from typing import Any, Awaitable, Callable, Dict
from aiogram.types import Message
from db_api import api_profile_async, api_chat_session_async


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
        profile = await api_profile_async.get_or_create_profile(
            tgid=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            url=user.url
        )
        session_profile = await api_chat_session_async.get_or_create_session(profile, profile.ai_model_id)
        data['user_profile'] = profile
        data['session_profile'] = session_profile

        return await handler(event, data)