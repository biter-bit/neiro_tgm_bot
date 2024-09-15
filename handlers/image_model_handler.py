from aiogram import Router, F
from aiogram.types import Message, InputFile, FSInputFile, BufferedInputFile, URLInputFile
from utils.models import Profile
from utils.enum import AiModelName, MjOption
from utils.db_api import get_or_create_session, active_generic_in_session, deactivate_generic_in_session, subtracting_count_request_to_model_mj, create_image_query
from utils.features import check_balance_profile
from PIL import Image
from io import BytesIO
from services import nlp_translator, midjourney_obj
from aiogram.fsm.context import FSMContext
from states.type_generation import TypeState
import httpx
import asyncio
from utils.callbacks import MJCallback
from buttons.mjoption_ib import create_inline_kb_for_image

image_router = Router()

image_models = [
    AiModelName.MIDJOURNEY.value,
]

@image_router.message(TypeState.image)
async def generate_image_model(message: Message, user_profile: Profile, state: FSMContext):
    """Обработай текстовые сообщения пользователей, которые являются prompt для нейронок изображений"""
    session_profile = await get_or_create_session(user_profile, user_profile.ai_model_id)
    if session_profile.active_generation:
        await message.delete()
        return await message.answer('Генерация активна')

    current_model = user_profile.ai_model_id

    if user_profile.tariffs.name == "Free":
        return await message.answer("Для доступа к этой модели поменяйте тариф!")
    else:
        if not check_balance_profile(user_profile):
            return await message.answer("Пополните баланс!")

    if current_model == AiModelName.MIDJOURNEY.value:
        await active_generic_in_session(session_profile.id)
        content = await nlp_translator.async_translate(text=message.text)
        result = await midjourney_obj.async_generate_image(content['result'])
        image_query = await create_image_query(result['prompt'], session_profile.id, result['jobid'])
        while True:
            result_task = await midjourney_obj.async_get_result_task(result)
            if result_task['status'] == 'failed':
                await message.answer("Попробуйте сделать запрос снова")
                # response_image = await client.get(content_task['attachments'][0]['url'])
                # image_stream = BytesIO(response_image.content)
                # image = Image.open(image_stream)
                # image.save("output_image.png")
                break
            elif result_task['status'] == 'completed':
                inline_kb = create_inline_kb_for_image(image_query.id)
                await message.answer_photo(
                    URLInputFile(result_task['attachments'][0]['url']),
                    caption='Вот изображение!',
                    reply_markup=inline_kb
                )
                await subtracting_count_request_to_model_mj(user_profile.id)
                break
            await asyncio.sleep(5)
            continue
        await deactivate_generic_in_session(session_profile.id)

@image_router.callback_query(MJCallback.filter(F.action == MjOption.VARIATION))
async def generate_variation_image_model(message: Message, user_profile: Profile, state: FSMContext):
    pass