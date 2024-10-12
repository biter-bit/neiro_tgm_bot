from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.enum import AdminButton
from utils.callbacks import GenerateLinkCallback, StatisticCallback, DownloadDBCallback, CreateRefLinkCallback

async def create_inline_kb_admin() -> InlineKeyboardMarkup:
    """Верни основную клавиатуру бота телеграм"""

    builder = InlineKeyboardBuilder()

    builder.button(text=AdminButton.GENERATE_LINK.value, callback_data=GenerateLinkCallback())
    builder.button(text=AdminButton.STATISTIC.value, callback_data=StatisticCallback())
    builder.button(text=AdminButton.DB_DOWNLOAD.value, callback_data=DownloadDBCallback())

    builder.adjust(1, 1, 1)

    return builder.as_markup()

async def create_inline_kb_generate_link() -> InlineKeyboardMarkup:
    """Верни основную клавиатуру бота телеграм"""

    builder = InlineKeyboardBuilder()

    builder.button(text=AdminButton.CREATE.value, callback_data=CreateRefLinkCallback())
    builder.button(text=AdminButton.STATISTIC.value, callback_data=StatisticCallback())

    builder.adjust(2)

    return builder.as_markup()