from config import settings

import asyncio
from aiogram import Bot, Dispatcher

from handlers import main_router
from utils import create_tables
from middlewares import ProfileMiddleware, CounterMiddleware


async def main():
    """Запусти бота"""
    create_tables()
    bot = Bot(settings.TOKEN_TELEGRAM_BOT)
    dp = Dispatcher(bot=bot)

    dp.message.middleware.register(CounterMiddleware())
    # dp.callback_query.middleware(ProfileMiddleware())
    dp.update.middleware(ProfileMiddleware())

    dp.include_router(main_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())