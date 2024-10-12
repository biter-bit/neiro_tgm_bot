from db_api.models import Profile, ChatSession
from PIL import Image
import os
import hashlib
from typing import Optional
from services import bot, logger
from utils.enum import AiModelName
from uuid import UUID
from db_api import api_profile_async, api_image_query_async, api_chat_session_async
from utils.cache import set_cache_profile, serialization_profile, get_cache_profile, deserialization_profile
import httpx
import json
from utils.enum import Errors
import sqlalchemy
from aiogram.types import Message, User
import pandas
from config import settings

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

async def finish_generation_image(url_photo: str, image_id: UUID, profile: Profile) -> Profile:
    """Сделай все основные действий после генерации"""
    await api_image_query_async.save_answer_query(url_photo, image_id)
    if profile.ai_model_id == AiModelName.MIDJOURNEY_5_2.value() and profile.mj_daily_limit_5_2 > 0:
        profile = await api_profile_async.subtracting_count_request_to_model_mj(profile.id, "5.2")
    elif profile.ai_models_id == AiModelName.MIDJOURNEY_6_0.value() and profile.mj_daily_limit_6_0 > 0:
        profile = await api_profile_async.subtracting_count_request_to_model_mj(profile.id, "6.0")
    return profile

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
    elif profile.ai_models_id.code == "o1-preview" and profile.chatgpt_o1_preview_daily_limit != 0:
        return True
    elif profile.ai_models_id.code == "o1-mini" and profile.chatgpt_o1_mini_daily_limit != 0:
        return True
    return False

async def check_start_text_generate(message: Message, user_profile: Profile, session_profile: ChatSession) -> dict:
    if session_profile.active_generation:
        await message.delete()
        return {'text': 'Генерация активна', 'status': True}
    elif user_profile.tariffs.name == "Free" and user_profile.ai_model_id in ("gpt-4o", "o1-mini", "o1-preview"):
        return {'text': "Для доступа к этой модели поменяйте тариф!", 'status': True}
    elif not check_limits_for_free_tariff(user_profile):
        return {'text': "Вы превысили лимит запросов в сутки для этой модели!", 'status': True}
    else:
        return {'text': '', 'status': False}

async def check_profile_in_cache(user: User):
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
    return profile

async def generic_table_excel():
    data = {
        "Name": ["Igor", "Slava"],
        "Age": [23, 25]
    }
    df = pandas.DataFrame(data)
    file_path = f"{settings.PATH_WORK}/example.xlsx"
    df.to_excel(file_path, index=False)
    return file_path

async def generic_html(data_dict: dict):
    data = f"""
    <!doctype html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport"
              content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <link rel="stylesheet" href="/static/css/bootstrap.min.css">
        <title>Отчёт по ссылкам</title>
    </head>
    <body>
        <div class="container">
            <h3 class="h4 text-center mt-4">Статистика текущего дня</h3>
            <div>
                👥 <b>Пользователи:</b><br>
                ├ Всего: {data_dict["count_users"]}<br>
                └ Реф. ссылки: {data_dict["count_ref_links"]}<br><br>
                📈 <b>Новые за сутки:</b><br>
                ├ Всего: {data_dict["count_new_users_for_day"]}<br>
                ├ С реф. ссылок: {data_dict["count_new_users_for_day_with_ref_links"]}<br>
                └ С поиска: 1396<br><br>
                🎓 <b>Обучение:</b><br>
                ├ Всего: 76776<br>
                └ За сутки: 11<br><br>
                📊<b>MAU:</b><br>
                ├ За день: 10890<br>
                └ За 30 дней: 202354<br><br>
                🏃 <b>Статистика за сутки по нейросетям:</b><br>
                ├ Всего запросов: 42247<br>
                ├ ChatGPT 3.5: 163<br>
                ├ ChatGPT 4: 0<br>
                ├ ChatGPT 4 o: 1<br>
                ├ ChatGPT 4 turbo: 0<br>
                ├ ЯндексGPT: 0<br>
                ├ ЯндексGPT Lite: 0<br>
                ├ Bard: 41567<br>
                ├ Claude Haiku: 0<br>
                ├ Claude Sonnet: 0<br>
                ├ Claude Opus: 0<br>
                ├ StableDiffusion: 429<br>
                ├ DallE-2: 0<br>
                ├ DallE-3: 2<br>
                ├ Midjourney: 1<br>
                ├ Kandinsky: 84<br>
                ├ Текст в видео: 0<br>
                ├ Изображение в видео: 0<br>
                ├ Удаление фона видео: 0<br>
                ├ Видео в мульт: 0<br>
                ├ PicaArt: 0<br>
                ├ Запросы ГПТ из чата: 38<br>
                └ Запросы IMG из чата: 7<br><br>
                👨‍🎓 <b>Статистика за сутки по сервисам:</b><br>
                ├ Для учебы: 11<br>
                │├ Генерация работ ChatGpt: 5<br>
                │├ Генерация работ Gemini: 6<br>
                │├ Генерация работ Claude: 0<br>
                │├ Рерайтинг: 0<br>
                │├ Решение по фото: 0<br>
                │└ Решение по фото PRO: 5<br>
                ├ Для работы: 0<br>
                │├ Генерация статьи: 0<br>
                │└ Анализ по ключу: 0<br>
                ├ Другие: 0<br>
                │├ Youtube Summary: 0<br>
                │├ Текст в речь: 0<br>
                │├ Речь в текст: 0<br>
                │├ Антиплагиат: 0<br>
                │├ Таро: 2<br>
                └┴ Удаление фона: 0<br><br>
                💰 <b>Платежи:</b><br>
                ├ Подписок Telegram Stars: 30<br>
                │├ Продажи подписок: 0шт на сумму 0₽<br>
                │├ Продажи токенов: 1000₽<br>
                │├ Покупок за 660 ⭐️ : 0<br>
                │├ Покупок за 1100 ⭐️: 0<br>
                │├ Покупок за 2000 ⭐️: 0<br>
                │├ Покупок за 3500 ⭐️: 0<br>
                │├ Средний чек: 0₽<br>
                │└ Общий оборот: 1000₽<br>
                │<br>
                ├ Подписок Robokassa: 589<br>
                │├ Новых подписок: 5шт на сумму 2450₽<br>
                │├ Продажи токенов: 0₽<br>
                │├ Покупок за 450₽: 5<br>
                │├ Покупок за 990₽: 0<br>
                │├ Покупок за 1800₽: 0<br>
                │├ Покупок за 3200₽: 0<br>
                │├ Продлений: 5<br>
                │├ Средний чек: 490₽<br>
                └└ Общий оборот: 2450₽
            </div>
        </div>
    </body>
    </html>
    """
    with open("my_page.html", "w") as file:
        file.write(data)
    return f'{settings.PATH_WORK}/my_page.html'

async def get_statistic():
    file_path = await generic_html()
    return file_path


async def get_session_for_profile(profile: Profile, ai_model_id: int) -> ChatSession:
    try:
        session_profile = await api_chat_session_async.get_or_create_session(profile, ai_model_id)
    except sqlalchemy.exc.IntegrityError as e:
        logger.info(f"Профиль {profile.tgid} не найден. Поэтому был создан новый.")
        profile = await api_profile_async.get_or_create_profile(
            tgid=profile.id,
            username=profile.username,
            first_name=profile.first_name,
            last_name=profile.last_name,
            url=profile.url
        )
        await set_cache_profile(profile.tgid, await serialization_profile(profile))
        session_profile = await api_chat_session_async.get_or_create_session(profile, ai_model_id)
    return session_profile

def check_balance_profile(profile: Profile) -> bool:
    """Проверь баланс пользователя и узнай, может он сделать запрос к нейросети или нет"""
    if profile.ai_models_id.code == "mj-5-2" and profile.mj_daily_limit_5_2 != 0:
        return True
    elif profile.ai_models_id.code == "mj-6-0" and profile.mj_daily_limit_6_0 != 0:
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