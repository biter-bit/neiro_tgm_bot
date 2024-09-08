"""Пакет с обработчиками сообщений телеграма"""

from aiogram import Router

from .start_handler import start_router
from .choice_model_handler import choice_model_router
from .info_profile_handler import info_profile_router
from .generic_handler import generic_router

main_router = Router()
main_router.include_routers(start_router)
main_router.include_routers(choice_model_router)
main_router.include_routers(info_profile_router)
main_router.include_routers(generic_router)