from typing import Tuple

from tgbot_app.db_api.models import Profile, ChatSession
from PIL import Image
import os
import hashlib
from tgbot_app.services import bot
from utils.enum import AiModelName
from uuid import UUID
from db_api import api_profile_async, api_image_query_async

async def finish_generation_image(url_photo: str, image_id: UUID, profile_id: int) -> str:
    """Сделай все основные действий после генерации"""
    await api_image_query_async.save_answer_query(url_photo, image_id)
    await api_profile_async.subtracting_count_request_to_model_mj(profile_id)
    return "Ok"

def check_status_generic(session_profile: ChatSession) -> dict:
    """Проверь статус генерации у пользователя."""
    access_allowed = True
    status_denied = False
    error_active_generation = f"You have already activated generation. Wait for it to complete."
    if not session_profile.active_generation:
        return {"status": access_allowed, "result": "Ok"}
    else:
        return {"status": status_denied, "result": error_active_generation}

def check_access_for_generic(user_profile: Profile, session_profile: ChatSession) -> dict:
    """Проверь доступ пользователя для генерации."""
    error_balance_free = f"Top up your balance. Available to you {user_profile.chatgpt_4o_mini_daily_limit} generations."
    error_balance_not_free = f"Top up your balance."
    error_tariff = f"Model {user_profile.ai_model_id} is not available for tariff {user_profile.tariffs.name}"
    access_allowed = True
    status_denied = False

    status_generic = check_status_generic(session_profile)
    if not status_generic["status"]:
        return status_generic

    if user_profile.tariffs.name == "Free":
        if user_profile.ai_model_id == AiModelName.GPT_4_O_MINI.value:
            if check_balance_profile(user_profile):
                return {"status": access_allowed, "result": "Ok"}
            else:
                return {"status": status_denied, "result": error_balance_free}
        else:
            return {"status": status_denied, "result": error_tariff}
    else:
        if check_balance_profile(user_profile):
            return {"status": access_allowed, "result": "Ok"}
        else:
            return {"status": status_denied, "result": error_balance_not_free}

def get_bot():
    """Верни экземпляр бота"""
    return bot

def check_limits_for_free_tariff(profile: Profile):
    """Проверь хватает ли пользователю c тарифом Free сделать запрос для генерации"""
    if profile.ai_models_id.code == "gpt-4o-mini" and profile.chatgpt_4o_mini_daily_limit > 0:
        return True
    return False

def check_balance_profile(profile: Profile) -> bool:
    """Проверь баланс пользователя и узнай, может он сделать запрос к нейросети или нет"""
    if profile.ai_models_id.code == "mj" and profile.mj_daily_limit != 0:
        return True
    elif profile.ai_models_id.code == "gpt-4o" and profile.chatgpt_4o_daily_limit != 0:
        return True
    elif profile.ai_models_id.code == "gpt-4o-mini" and profile.chatgpt_4o_mini_daily_limit != 0:
        return True
    return False

def get_image_part(image_path, part_number, output_dir, name_file_photo):
    # Проверяем корректность номера части
    if part_number not in [1, 2, 3, 4]:
        raise ValueError("part_number должен быть в диапазоне от 1 до 4.")

    # Открываем изображение
    image = Image.open(image_path)

    # Получаем размеры изображения
    width, height = image.size

    # Рассчитываем размеры каждой части
    half_width = width // 2
    half_height = height // 2

    # Определяем координаты частей
    parts = {
        1: (0, 0, half_width, half_height),  # Верхний левый угол
        2: (half_width, 0, width, half_height),  # Верхний правый угол
        3: (0, half_height, half_width, height),  # Нижний левый угол
        4: (half_width, half_height, width, height)  # Нижний правый угол
    }

    # Обрезаем изображение, чтобы получить нужную часть
    part_coords = parts[part_number]
    part_image = image.crop(part_coords)

    # Формируем путь для сохранения части изображения
    output_path = os.path.join(output_dir, f"{name_file_photo}.png")

    # Сохраняем полученную часть изображения
    part_image.save(output_path)

    return output_path

def create_safe_filename(url, suffix=".png"):
    # Генерация хеша из URL
    hash_object = hashlib.md5(url.encode())
    # Превращаем хеш в строку
    hash_name = hash_object.hexdigest()
    # Возвращаем безопасное имя файла с нужным суффиксом
    return f"{hash_name}{suffix}"