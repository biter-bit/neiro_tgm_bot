from .async_api import (DBApiAsync, ApiTariffAsync, ApiProfileAsync, ApiAiModelAsync, ApiImageQueryAsync,
                     ApiTextQueryAsync, ApiChatSessionAsync)
from .sync_api import DBApiSync

db_api_sync_obj = DBApiSync()
db_api_async_obj = DBApiAsync()
api_tariff_async = ApiTariffAsync()
api_profile_async = ApiProfileAsync()
api_ai_model_async = ApiAiModelAsync()
api_image_query_async = ApiImageQueryAsync()
api_text_query_async = ApiTextQueryAsync()
api_chat_session_async = ApiChatSessionAsync()

__all__ = [
    db_api_sync_obj, db_api_async_obj, api_profile_async, api_tariff_async, api_ai_model_async, api_text_query_async,
    api_chat_session_async, api_image_query_async
]