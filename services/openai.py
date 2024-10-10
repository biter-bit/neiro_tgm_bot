from openai import OpenAI, AsyncOpenAI
import asyncio
import httpx

class ChatGPT:
    def __init__(self, token: str, base_url: str, token_not_off: str, base_url_not_off, proxy_url: str):
        # self.client_chat_gpt = OpenAI(api_key=token, base_url=base_url)
        limits = httpx.Limits(max_connections=None, max_keepalive_connections=None)
        self.async_client_chat_gpt = AsyncOpenAI(api_key=token, base_url=base_url, http_client=httpx.AsyncClient(proxies=proxy_url, limits=limits))
        self.async_not_official_client_chat_gpt = AsyncOpenAI(api_key=token_not_off, base_url=base_url_not_off, http_client=httpx.AsyncClient(proxies=proxy_url, limits=limits))

    async def async_generate_text(self, ai_model: str, context: list, prompt: str):
        new_messages = {"role": "user", "content": prompt}
        context.append(new_messages)
        try:
            response = await asyncio.wait_for(
                self.async_not_official_client_chat_gpt.chat.completions.create(model=ai_model, messages=context),
                timeout=10
            )
            return response
        except asyncio.TimeoutError:
            response = await self.async_client_chat_gpt.chat.completions.create(model=ai_model, messages=context)
            return response
        except Exception:
            response = await self.async_client_chat_gpt.chat.completions.create(model=ai_model, messages=context)
            return response

    async def async_generate_image_to_text(self, ai_model: str, context: list, prompt: list):
        new_messages = {"role": "user", "content": prompt}
        context.append(new_messages)
        try:
            response = await asyncio.wait_for(
                self.async_not_official_client_chat_gpt.chat.completions.create(model=ai_model, messages=context),
                timeout=30
            )
            return response
        except asyncio.TimeoutError:
            response = await self.async_client_chat_gpt.chat.completions.create(model=ai_model, messages=context)
            return response
        except Exception:
            response = await self.async_client_chat_gpt.chat.completions.create(model=ai_model, messages=context)
            return response