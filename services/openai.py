from openai import OpenAI, AsyncOpenAI
import asyncio
import httpx
from logging import Logger
from utils.enum import AiModelName

class ChatGPT:
    def __init__(self, token: str, base_url: str, token_not_off: str, base_url_not_off, proxy_url: str, logger: Logger):
        limits = httpx.Limits(max_connections=None, max_keepalive_connections=None)
        self.logger = logger
        self.async_client_chat_gpt = AsyncOpenAI(api_key=token, base_url=base_url, http_client=httpx.AsyncClient(proxies=proxy_url, limits=limits))
        self.async_not_official_client_chat_gpt = AsyncOpenAI(api_key=token_not_off, base_url=base_url_not_off, http_client=httpx.AsyncClient(proxies=proxy_url, limits=limits))

    async def async_generate_text(self, ai_model: str, context: list, prompt: str, profile_id: int, max_retries: int = 3):
        timeout = 30
        if ai_model in (AiModelName.GPT_O1_MINI.value, AiModelName.GPT_O1_PREVIEW.value):
            timeout = 500
        new_messages = {"role": "user", "content": prompt}
        context.append(new_messages)
        for attempt in range(max_retries):
            try:
                response = await asyncio.wait_for(
                    self.async_not_official_client_chat_gpt.chat.completions.create(model=ai_model, messages=context, temperature=0),
                    timeout=timeout
                )
                return response
            except Exception as e:
                self.logger.error(f"Пользователь id - {profile_id}. Попытка {attempt + 1}/{max_retries} не удалась: {e}")
                if attempt == max_retries - 1:
                    raise

                try:
                    response = await asyncio.wait_for(
                        self.async_client_chat_gpt.chat.completions.create(model=ai_model, messages=context),
                        timeout=timeout
                    )
                    return response
                except Exception as e2:
                    self.logger.error(f"Пользователь id - {profile_id}. Официальный клиент: попытка {attempt + 1}/{max_retries} не удалась: {e2}")
                    if attempt == max_retries - 1:
                        self.logger.error(f"Пользователь id - {profile_id}. Генерация текста не удалась. Причина - {e2}")

            await asyncio.sleep(2)