from openai import OpenAI, AsyncOpenAI
from config import settings

openai_client = OpenAI(api_key=settings.OPENAI_API_KEY, base_url="https://apisbost.top/v1/")
openai_client_async = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)