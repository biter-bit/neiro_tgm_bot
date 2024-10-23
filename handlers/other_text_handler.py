from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from db_api.models import Profile
from utils.states import TypeAiState
from handlers.text_model_handler import generate_text_model
from handlers.image_model_handler import generate_image_model

other_router = Router()

@other_router.message()
async def other_text_handler(message: Message, state: FSMContext, user_profile: Profile):
    if user_profile.ai_models_id.type == "text":
        await state.set_state(TypeAiState.text)
        await generate_text_model(message=message, user_profile=user_profile)
    else:
        await state.set_state(TypeAiState.image)
        await generate_image_model(message=message, user_profile=user_profile)