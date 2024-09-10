from openai import OpenAI, AsyncOpenAI

class ChatGPT:
    def __init__(self, token: str, base_url: str):
        self.client_chat_gpt = OpenAI(api_key=token, base_url=base_url)
        # self.async_client_chat_gpt = AsyncOpenAI(api_key=token, base_url=base_url)

    async def async_generate_text(self, ai_model: str, context: list, prompt: str):
        new_messages = {"role": "user", "content": prompt}
        context.append(new_messages)
        response = self.client_chat_gpt.chat.completions.create(
            model=ai_model,
            messages=context
        )
        return response