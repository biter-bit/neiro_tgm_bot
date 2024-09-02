from config import settings

import asyncio
from aiogram import Bot, Dispatcher

from handlers import main_router
from utils import create_tables
from middlewares import ProfileMiddleware, CounterMiddleware


async def main():
    """Запусти бота"""

    create_tables() # создаем таблицы бд
    bot = Bot(settings.TOKEN_TELEGRAM_BOT) # для работы с API Telegram
    dp = Dispatcher(bot=bot) # создаем обьект диспетчера для работы с callback и сообщениями бота telegram

    dp.message.middleware.register(CounterMiddleware()) # создаем middleware счетчик сообщений
    # dp.callback_query.middleware(ProfileMiddleware())
    dp.update.middleware(ProfileMiddleware()) # создаем middleware создание пользователя если нет

    dp.include_router(main_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())