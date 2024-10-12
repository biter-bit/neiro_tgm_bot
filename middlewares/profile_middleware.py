from aiogram import BaseMiddleware
from typing import Any, Awaitable, Callable, Dict, Optional
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, User
from db_api import api_profile_async
from db_api.models import Profile
from services import logger
from utils.enum import AiModelName
from utils.features import get_session_for_profile
from utils.cache import get_cache_profile, set_cache_profile, serialization_profile, deserialization_profile
from states.type_generation import TypeAiState

class ProfileMiddleware(BaseMiddleware):
    """
    Представляет из себя класс по подготовке пользователя для работы с ботом,
    который выполняется до и после обработчика aiogram.
    """
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        """Подготовь пользователя для работы с ботом перед каждым созданием обьекта middleware."""

        user: User = event.from_user

        # проверяем есть ли данные о пользователе в кэше
        cache_value: Optional[str] = await get_cache_profile(user.id)
        if cache_value:
            profile: Optional[Profile] = await deserialization_profile(cache_value)
        else:
            profile: Optional[Profile] = await api_profile_async.get_or_create_profile(
                tgid=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                url=user.url
            )
            await set_cache_profile(user.id, await serialization_profile(profile))

        # проверяем и устанавливаем состояние типа ai
        state: FSMContext = data.get('state')
        current_state: Optional[str] = await state.get_state()
        if current_state is None or profile.ai_models_id.code in AiModelName.get_list_text_value_model():
            await state.set_state(TypeAiState.text)
            logger.info(f"Состояние пользователя {user.id} установлено на 'text'")
        elif profile.ai_models_id.code in AiModelName.get_list_image_value_model():
            await state.set_state(TypeAiState.image)
            logger.info(f"Состояние пользователя {user.id} установлено на 'image'")

        data['user_profile'] = profile

        return await handler(event, data)