from .openai import ChatGPT
from .nlp_translator import Translator
from .midjourney import MJ
from config import settings
from .payment import Robokassa
from aiogram import Bot, Dispatcher
from .logger_service import create_logger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.fsm.storage.memory import MemoryStorage
import aioredis

logger = create_logger(settings.LEVEL_LOGGER)

bot = Bot(token=settings.TOKEN_TELEGRAM_BOT)
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage) # создаем обьект диспетчера для работы с callback и сообщениями бота telegram
redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", decode_responses=True)
chat_gpt = ChatGPT(
    token=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_BASE_URL,
    token_not_off=settings.NOT_OFFICIAL_OPENAI_API_KEY,
    base_url_not_off=settings.NOT_OFFICIAL_OPENAI_BASE_URL,
    proxy_url=settings.PROXY,
    logger=logger
)
nlp_translator = Translator(token=settings.RAPID_API_TOKEN, proxy=settings.PROXY)
midjourney_obj = MJ(token=settings.USEAPI_API_KEY)
robokassa_obj = Robokassa(
    login=settings.ROBOKASSA_LOGIN,
    password_1=settings.ROBOKASSA_PASS_1,
    password_2=settings.ROBOKASSA_PASS_2
)