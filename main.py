import asyncio
from handlers import main_router
from db_api import db_api_sync_obj
from middlewares import ProfileMiddleware, MainMiddleware, RedirectGroupMiddleware
from services import bot, dp, scheduler
from utils.scheduler import update_limits, check_subscription
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

# Запуск APScheduler
async def on_startup():
    """Запусти фоновые задачи"""
    scheduler.add_job(update_limits, IntervalTrigger(minutes=1)) # обновляет ежедневные лимиты
    scheduler.add_job(check_subscription, IntervalTrigger(minutes=28)) # проверяет актуальность подписки и выполняет соответствующие действия
    scheduler.start()

async def main():
    """Запусти бота"""
    db_api_sync_obj.create_tables() # создаем таблицы

    dp.message.middleware(ProfileMiddleware()) # создаем middleware создание пользователя если нет
    dp.callback_query.middleware(ProfileMiddleware()) # создаем middleware создание пользователя если нет

    dp.message.middleware(MainMiddleware()) # создаем middleware проверка подписки на каналы
    dp.callback_query.middleware(MainMiddleware()) # создаем middleware проверка подписки на каналы

    dp.message.middleware(RedirectGroupMiddleware()) # создаем middleware перевода групповых запросов

    dp.include_router(main_router) # включаем основной router

    dp.startup.register(on_startup) # создаем фоновые задачи

    await dp.start_polling(bot) # запускаем бота

if __name__ == '__main__':
    asyncio.run(main())