from sys import prefix

from aiogram.filters.callback_data import CallbackData
from utils.enum import MjOption, PaymentName, AiModelName
from uuid import UUID

class StatisticCallback(CallbackData, prefix="statistic"):
    pass

class GenerateLinkCallback(CallbackData, prefix="generate_link"):
    pass

class DownloadDBCallback(CallbackData, prefix="download_db"):
    pass

class CreateRefLinkCallback(CallbackData, prefix="create_ref_link"):
    pass

class MJCallback(CallbackData, prefix="mj"):
    action: MjOption
    index: int
    mj_query_id: UUID

class PaymentCallback(CallbackData, prefix="payment"):
    option: PaymentName

class ModeCallback(CallbackData, prefix="mode"):
    action: str