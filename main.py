import asyncio
from handlers import main_router
from tgbot_app.db_api import db_api_sync_obj
from middlewares import ProfileMiddleware, MainMiddleware, RedirectGroupMiddleware
from tgbot_app.services import bot, dp

async def main():
    """Запусти бота"""
    db_api_sync_obj.create_tables() # создаем таблицы
    dp.message.middleware(ProfileMiddleware()) # создаем middleware создание пользователя если нет
    dp.message.middleware(MainMiddleware()) # создаем middleware проверка подписки на каналы
    dp.callback_query.middleware(ProfileMiddleware()) # создаем middleware создание пользователя если нет
    dp.callback_query.middleware(MainMiddleware()) # создаем middleware проверка подписки на каналы
    dp.message.middleware(RedirectGroupMiddleware()) # создаем middleware перевода групповых запросов
    dp.include_router(main_router) # включаем основной router
    await dp.start_polling(bot) # запускаем бота

if __name__ == '__main__':
    asyncio.run(main())