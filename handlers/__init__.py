"""Пакет с обработчиками сообщений телеграма"""

from aiogram import Router

from .start_hundler import start_router
from .choice_model_handler import choice_model_router

main_router = Router()
main_router.include_routers(start_router)
main_router.include_routers(choice_model_router)