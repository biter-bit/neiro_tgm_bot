from .openai import ChatGPT
from .nlp_translator import Translator
from .midjourney import MJ
from config import settings
from .payment import Robokassa

chat_gpt = ChatGPT(token=settings.OPENAI_API_KEY, base_url=settings.OPENAI_BASE_URL)
nlp_translator = Translator(token=settings.RAPID_API_TOKEN, proxy=settings.PROXY)
midjourney_obj = MJ(token=settings.USEAPI_API_KEY)
robokassa_obj = Robokassa(
    login=settings.ROBOKASSA_LOGIN,
    password_1=settings.ROBOKASSA_PASS_1,
    password_2=settings.ROBOKASSA_PASS_2
)