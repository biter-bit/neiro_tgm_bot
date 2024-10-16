from aiogram import BaseMiddleware
from typing import Any, Awaitable, Callable, Dict, Optional
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, User
from db_api import api_profile_async, api_ref_link_async
from db_api.models import Profile
from services import logger
from utils.enum import AiModelName
from utils.cache import get_cache_profile, set_cache_profile, serialization_profile, deserialization_profile
from utils.states import TypeAiState
from config import settings
from sqlalchemy.exc import IntegrityError

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

        ref_link_id = None
        if isinstance(event, Message):
            try:
                list_arg = event.text.split(' ')
                if len(list_arg) == 2:
                    num_link = int(list_arg[1])
                    ref_link = await api_ref_link_async.add_click(f'{settings.USERNAME_BOT}?start={num_link}')
                    ref_link_id = ref_link.id
            except TypeError as e:
                logger.error("Команда /start с данным аргументом не работает.")
            except ValueError as e:
                logger.error("Забей")
            except AttributeError as e:
                logger.error("В event.text значение None.")

        # проверяем есть ли данные о пользователе в кэше
        cache_value: Optional[str] = await get_cache_profile(user.id)
        if cache_value:
            profile: Optional[Profile] = await deserialization_profile(cache_value)
        else:
            profile: Optional[Profile] = await api_profile_async.get_profile(user.id)
            if not profile:
                try:
                    profile: Optional[Profile] = await api_profile_async.create_profile(
                        tgid=user.id,
                        username=user.username,
                        first_name=user.first_name,
                        last_name=user.last_name,
                        url=user.url,
                        referal_link_id=ref_link_id
                    )
                except IntegrityError as e:
                    logger.error(f"Ошибка создания профиля: {e}")
                    profile: Optional[Profile] = await api_profile_async.get_profile(user.id)
                if ref_link_id:
                    await api_ref_link_async.add_count_new_users(ref_link_id)
            await set_cache_profile(user.id, await serialization_profile(profile))

        # проверяем и устанавливаем состояние типа ai
        state: FSMContext = data.get('state')
        current_state: Optional[str] = await state.get_state()
        if current_state is None:
            if profile.ai_models_id.type == "text":
                await state.set_state(TypeAiState.text)
                logger.info(f"Состояние пользователя {user.id} установлено на 'text'")
            elif profile.ai_models_id.type == "image":
                await state.set_state(TypeAiState.image)
                logger.info(f"Состояние пользователя {user.id} установлено на 'image'")

        data['user_profile'] = profile

        return await handler(event, data)