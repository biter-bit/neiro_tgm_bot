from aiogram.filters.callback_data import CallbackData
from utils.enum import MjOption
from uuid import UUID

class MJCallback(CallbackData, prefix="mj"):
    action: MjOption
    index: int
    mj_query_id: UUID