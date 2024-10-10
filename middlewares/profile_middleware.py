from aiogram import BaseMiddleware
from typing import Any, Awaitable, Callable, Dict
from aiogram.types import Message, CallbackQuery
from db_api import api_profile_async, api_chat_session_async
from services import logger
from utils.enum import AiModelName
import sqlalchemy
from utils.cache import get_cache_profile, set_cache_profile, serialization_profile, deserialization_profile

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
        cache_value = await get_cache_profile(user.id)
        if cache_value:
            profile = await deserialization_profile(cache_value)
        else:
            profile = await api_profile_async.get_or_create_profile(
                tgid=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                url=user.url
            )
            await set_cache_profile(user.id, await serialization_profile(profile))

        if isinstance(event, CallbackQuery) and hasattr(data["callback_data"], "action") and data["callback_data"].action in AiModelName.get_list_value():
            ai_model_id = data["callback_data"].action
        else:
            ai_model_id = profile.ai_model_id

        try:
            session_profile = await api_chat_session_async.get_or_create_session(profile, ai_model_id)
        except sqlalchemy.exc.IntegrityError as e:
            logger.info(f"Профиль {profile.tgid} не найден. Поэтому был создан новый.")
            profile = await api_profile_async.get_or_create_profile(
                tgid=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                url=user.url
            )
            await set_cache_profile(user.id, await serialization_profile(profile))
            session_profile = await api_chat_session_async.get_or_create_session(profile, ai_model_id)

        data['user_profile'] = profile
        data['session_profile'] = session_profile

        return await handler(event, data)