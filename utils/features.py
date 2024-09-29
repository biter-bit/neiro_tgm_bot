from db_api.models import Profile, ChatSession
from PIL import Image
import os
import hashlib
from services import bot
from utils.enum import AiModelName
from uuid import UUID
from db_api import api_profile_async, api_image_query_async
import httpx
import json
from utils.enum import Errors

def create_photo(photo_byte: bytes, path_file: str):
    """Создай фото из байтов"""
    with open(path_file, 'wb') as image_file:
        image_file.write(photo_byte)
    return "Ok"

async def make_request(url):
    """Получи данные get запроса"""
    try:
        async with httpx.AsyncClient() as client:
            result = await client.get(url)
            return {
                "status_code": result.status_code,
                "result": result
            }
    except httpx.HTTPStatusError as e:
        return {
            "status_code": e.response.status_code,
            "result": e.response.text
        }

    except httpx.TimeoutException:
        return {
            "status_code": 408,  # Тайм-аут
            "result": "Запрос превышает время ожидания"
        }
    except httpx.RequestError as e:
        return {
            "status_code": 500,  # Общая ошибка запроса
            "result": str(e)
        }
    except json.JSONDecodeError:
        return {
            "status_code": 500,  # Ошибка декодирования JSON
            "result": "Ошибка декодирования JSON"
        }

async def finish_generation_image(url_photo: str, image_id: UUID, profile: Profile) -> str:
    """Сделай все основные действий после генерации"""
    await api_image_query_async.save_answer_query(url_photo, image_id)
    if profile.mj_daily_limit > 0:
        await api_profile_async.subtracting_count_request_to_model_mj(profile.id)
    return "Ok"

def check_status_generic(session_profile: ChatSession) -> dict:
    """Проверь статус генерации у пользователя."""
    if not session_profile.active_generation:
        return {"status": Errors.NON_ERROR.name, "result": Errors.NON_ERROR.value}
    else:
        return {"status": Errors.ERROR_ACTIVE_GENERATE.name, "result": Errors.ERROR_ACTIVE_GENERATE.value}

def check_access_for_generic(user_profile: Profile, session_profile: ChatSession) -> dict:
    """Проверь доступ пользователя для генерации."""

    status_generic = check_status_generic(session_profile)
    if status_generic["status"] != Errors.NON_ERROR.name:
        return status_generic

    if user_profile.tariffs.name == "Free":
        if user_profile.ai_model_id == AiModelName.GPT_4_O_MINI.value:
            if check_balance_profile(user_profile):
                return {"status": Errors.NON_ERROR.name, "result": Errors.NON_ERROR.value}
            else:
                return {"status": Errors.ERROR_BALANCE_FREE.name, "result": Errors.error_balance_free(str(user_profile.chatgpt_4o_mini_daily_limit))}
        else:
            return {"status": Errors.ERROR_TARIFF.name, "result": Errors.error_tariff(user_profile.ai_model_id, user_profile.tariffs.name)}
    else:
        if check_balance_profile(user_profile):
            return {"status": Errors.NON_ERROR.name, "result": Errors.NON_ERROR.value}
        else:
            return {"status": Errors.ERROR_BALANCE_PAID.name, "result": Errors.ERROR_BALANCE_PAID.value}

def get_bot():
    """Верни экземпляр бота"""
    return bot

def check_limits_for_free_tariff(profile: Profile):
    """Проверь хватает ли пользователю c тарифом Free сделать запрос для генерации"""
    if profile.ai_models_id.code == "gpt-4o-mini" and profile.chatgpt_4o_mini_daily_limit != 0:
        return True
    elif profile.ai_models_id.code == "gpt-4o" and profile.chatgpt_4o_daily_limit != 0:
        return True
    return False

def check_balance_profile(profile: Profile) -> bool:
    """Проверь баланс пользователя и узнай, может он сделать запрос к нейросети или нет"""
    if profile.ai_models_id.code in ("mj-6-0", "mj-5-2") and profile.mj_daily_limit != 0:
        return True
    elif profile.ai_models_id.code == "gpt-4o" and profile.chatgpt_4o_daily_limit != 0:
        return True
    elif profile.ai_models_id.code == "gpt-4o-mini" and profile.chatgpt_4o_mini_daily_limit != 0:
        return True
    return False

def delete_image(file_path: str):
    try:
        # Проверяем, существует ли файл
        if os.path.exists(file_path):
            os.remove(file_path)  # Удаляем файл
            print(f"Файл {file_path} успешно удалён.")
        else:
            print(f"Файл {file_path} не существует.")
    except Exception as e:
        print(f"Ошибка при удалении файла: {e}")

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