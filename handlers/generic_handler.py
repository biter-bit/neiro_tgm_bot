from aiogram import Router
from aiogram.types import Message, InputFile, FSInputFile, BufferedInputFile, URLInputFile
from utils.models import Profile
from utils.enum import AiModelName
from utils.db_api import get_or_create_session, create_text_query, get_text_messages_from_session, save_message
from config import settings
from services import openai_client
import httpx
import json
import asyncio
from openai import BadRequestError
from PIL import Image
from io import BytesIO

generic_router = Router()

@generic_router.message()
async def generate_run(message: Message, user_profile: Profile):
    """Обработай текстовые сообщения пользователей, которые являются prompt для нейронок"""

    if not message.text.startswith('/'):
        session_profile = await get_or_create_session(user_profile, user_profile.ai_model_id)
        try:
            if user_profile.ai_model_id == AiModelName.GPT_4_O_MINI.value:
                name_ai_model = AiModelName.GPT_4_O_MINI.value
                # url = 'https://api.openai.com/v1/chat/completions'
                # headers = {
                #     'Content-Type': 'application/json',
                #     'Authorization': f'Bearer {settings.OPENAI_API_KEY}'
                # }
                # json_data = {
                #     "model": "gpt-4o-mini",
                #     "messages": [
                #         {
                #             "role": "system",
                #             "content": "You are a helpful assistant."
                #         },
                #         {
                #             "role": "user",
                #             "content": message.text
                #         }
                #     ]
                # }
                # async with httpx.AsyncClient() as client:
                #     response = await client.post(url, headers=headers, json=json_data)
                #     content = json.loads(response.content)
                #     await message.answer(content["choices"][0]["message"]["content"])
                text_query = await create_text_query(message.text, session_profile.id)
                text_messages = await get_text_messages_from_session(session_profile.id, name_ai_model)
                new_messages = {"role": "user", "content": message.text}
                text_messages.append(new_messages)
                response = openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=text_messages
                )
                await save_message(response.choices[0].message.content, text_query.id)
                await message.answer(f"{response.choices[0].message.content}")

            if user_profile.ai_model_id == AiModelName.GPT_4_O.value:
                name_ai_model = AiModelName.GPT_4_O.value
                text_query = await create_text_query(message.text, session_profile.id)
                text_messages = await get_text_messages_from_session(session_profile.id, name_ai_model)
                new_messages = {"role": "user", "content": message.text}
                text_messages.append(new_messages)
                response = openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=text_messages
                )
                await save_message(response.choices[0].message.content, text_query.id)
                await message.answer(f"{response.choices[0].message.content}")
            if user_profile.ai_model_id == AiModelName.MIDJORNEY.value:
                await message.answer_photo(FSInputFile('output_image.png', 'output_image'), caption='Вот изображение!')
            if user_profile.ai_model_id == AiModelName.MIDJORNEY.value:
                url = 'https://api.useapi.net/v2/jobs/imagine'
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {settings.USEAPI_API_KEY}'
                }
                json_data = {
                    "prompt": message.text
                }
                async with httpx.AsyncClient(timeout=300) as client:
                    response = await client.post(url, headers=headers, json=json_data)
                    content = json.loads(response.content)
                    while True:
                        response_task = await client.get(f'https://api.useapi.net/v2/jobs/?jobid={content["jobid"]}', headers=headers)
                        content_task = json.loads(response_task.content)
                        if content_task['status'] == 'failed':
                            await message.answer("Попробуйте сделать запрос снова")
                            break
                        if content_task['status'] == "completed":
                            # response_image = await client.get(content_task['attachments'][0]['url'])
                            # image_stream = BytesIO(response_image.content)
                            # image = Image.open(image_stream)
                            # image.save("output_image.png")
                            await message.answer_photo(
                                URLInputFile(content_task['attachments'][0]['url']),
                                caption='Вот изображение!'
                            )
                            break
                        await asyncio.sleep(5)
                        continue
        except BadRequestError as error:
            if error.code == "context_length_exceeded":
                # logger.error("BadRequestError error | MAX CONTEXT")
                return {"status": "error", "code": "max_content", "result": "Превышен контекст"}

            # logger.error(f"BadRequestError error | {error}  {error.code}")
            return {"status": "error", "code": error.code, "result": ""}