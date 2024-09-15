from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.enum import MjOption
from utils.callbacks import MJCallback

def create_inline_kb_for_image(mj_query_id: str):
    builder = InlineKeyboardBuilder()

    for action in (MjOption.VARIATION, MjOption.UPSAMPLE):
        for idx in range(1, 5):
            builder.button(
                text=f"{action.value[0].upper()}{idx}",
                callback_data=MJCallback(action=action, index=idx, mj_query_id=mj_query_id),
            )

    builder.adjust(4, 4)

    return builder.as_markup()