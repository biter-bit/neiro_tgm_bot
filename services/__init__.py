from .openai import ChatGPT
from .nlp_translator import Translator
from .midjourney import MJ
from config import settings

chat_gpt = ChatGPT(token=settings.OPENAI_API_KEY, base_url=settings.OPENAI_BASE_URL)
nlp_translator = Translator(token=settings.RAPID_API_TOKEN, proxy=settings.PROXY)
midjourney_obj = MJ(token=settings.USEAPI_API_KEY)