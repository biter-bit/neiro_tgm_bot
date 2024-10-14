from aiogram import Router, F
from aiogram.types import Message, FSInputFile, CallbackQuery

from db_api import api_ref_link_async, api_profile_async
from utils.states import CreateRefLinkState, TypeAiState
from aiogram.fsm.context import FSMContext
from db_api.models import Profile
from aiogram.filters import Command
from utils.enum import AdminMessage, AiModelName, AdminButton
from utils.features import get_basic_statistic, get_ref_statistic
from buttons.admin_ib import create_inline_kb_admin, create_inline_kb_generate_link
from utils.callbacks import GenerateLinkCallback, DownloadDBCallback, StatisticCallback, CreateRefLinkCallback

admin_router = Router()

@admin_router.message(Command("admin"))
async def func_admin_handler(message: Message, user_profile: Profile):
    if not user_profile.is_admin:
        await message.answer(AdminMessage.NOT_ADMIN.value)
        return
    markup = await create_inline_kb_admin()
    await message.answer(AdminMessage.CHOOSE_ACTION.value, reply_markup=markup)

@admin_router.callback_query(GenerateLinkCallback.filter())
async def callback_generate_link(query: CallbackQuery):
    markup = await create_inline_kb_generate_link()
    await query.message.answer(AdminMessage.LINK_SECTION.value, reply_markup=markup)

@admin_router.callback_query(StatisticCallback.filter(F.option == AdminButton.STATISTIC))
async def callback_basic_statistics(query: CallbackQuery):
    stat = await get_basic_statistic()
    await query.message.answer(stat)

@admin_router.callback_query(StatisticCallback.filter(F.option == AdminButton.STATISTIC_REF))
async def callback_ref_statistics(query: CallbackQuery, user_profile: Profile):
    stat_list = await get_ref_statistic(user_profile.id)
    for stat in stat_list:
        await query.message.answer(stat)

@admin_router.callback_query(DownloadDBCallback.filter())
async def callback_download_db(query: CallbackQuery):
    await query.message.answer("download_db")

@admin_router.callback_query(CreateRefLinkCallback.filter())
async def callback_create_ref_link(query: CallbackQuery, state: FSMContext):
    await state.set_state(CreateRefLinkState.create)
    await query.message.answer(AdminMessage.INPUT_NAME_LINK.value)

@admin_router.message(CreateRefLinkState.create)
async def create_ref_link(message: Message, state: FSMContext, user_profile: Profile):
    ref_link = await api_ref_link_async.create_ref_link(message.text, user_profile.id)
    if user_profile.ai_models_id in AiModelName.get_list_text_value_model():
        await state.set_state(TypeAiState.text)
    else:
        await state.set_state(TypeAiState.image)
    await message.answer(f"Ваша ссылка:\n\n<i>{ref_link.link}</i>", parse_mode='HTML')