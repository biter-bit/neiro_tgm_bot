from aiogram import Router
from aiogram.types import Message, FSInputFile, CallbackQuery
from db_api.models import Profile
from aiogram.filters import Command
from utils.enum import AdminMessage
from utils.features import get_statistic
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
async def callback_generate_links(query: CallbackQuery):
    markup = await create_inline_kb_generate_link()
    await query.message.answer(AdminMessage.LINK_SECTION.value, reply_markup=markup)

@admin_router.callback_query(StatisticCallback.filter())
async def callback_statistics(query: CallbackQuery):
    await query.message.answer("statistic")
    # file_path = await get_statistic()
    # file = FSInputFile(file_path)
    # await query.message.answer_document(file)

@admin_router.callback_query(DownloadDBCallback.filter())
async def callback_download_db(query: CallbackQuery):
    await query.message.answer("download_db")

@admin_router.callback_query(CreateRefLinkCallback.filter())
async def callback_generate_links(query: CallbackQuery):
    await query.message.answer("create_ref_link")