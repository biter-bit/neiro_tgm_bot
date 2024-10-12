"""Пакет с обработчиками сообщений"""

from aiogram import Router

from .start_handler import start_router
from .choice_model_handler import choice_model_router
from .info_profile_handler import info_profile_router
from .text_model_handler import text_router
from .image_model_handler import image_router
from .reset_context_handler import reset_router
from .help_handler import help_router
from .subscription_handler import pay_router
from .group_handler import ask_router
from .admin_handler import admin_router

main_router = Router()

main_router.include_routers(
start_router, admin_router, reset_router, pay_router, help_router, ask_router, choice_model_router, info_profile_router,
    text_router, image_router
)