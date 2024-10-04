from db_api import api_profile_async

async def update_limits():
    result = await api_profile_async.update_limits_profile()
    return result

async def check_subscription():
    result = await api_profile_async.update_limits_profile()
    return result