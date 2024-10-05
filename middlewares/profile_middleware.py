from aiogram import BaseMiddleware
from typing import Any, Awaitable, Callable, Dict
from aiogram.types import Message, CallbackQuery
from db_api import api_profile_async, api_chat_session_async
from utils.enum import AiModelName
from services import redis
import json
from db_api.models import Profile, Tariff


class ProfileMiddleware(BaseMiddleware):
    """Представляет из себя класс по работе с пользователем, который выполняется до и после обработчика"""
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        """Создай пользователя, если его нет в базе данных"""
        user = event.from_user
        cache_value = await redis.get(user.id)
        if cache_value:
            profile_data = json.loads(cache_value)
            tariff = Tariff(**profile_data['tariffs'])
            profile_data['tariffs'] = tariff
            profile = Profile(**profile_data)
        else:
            profile = await api_profile_async.get_or_create_profile(
                tgid=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                url=user.url
            )
            await redis.set(user.id, json.dumps(profile.to_dict()))
        if isinstance(event, CallbackQuery) and hasattr(data["callback_data"], "action") and data["callback_data"].action in AiModelName.get_list_value():
            session_profile = await api_chat_session_async.get_or_create_session(profile, data["callback_data"].action)
        else:
            session_profile = await api_chat_session_async.get_or_create_session(profile, profile.ai_model_id)
        data['user_profile'] = profile
        data['session_profile'] = session_profile

        return await handler(event, data)