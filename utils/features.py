from utils.models import Profile

def check_limits_for_free_tariff(profile: Profile):
    """Проверь хватает ли пользователю c тарифом Free сделать запрос для генерации"""
    if profile.ai_models_id.code == "gpt-4o-mini" and profile.chatgpt_4o_mini_daily_limit > 0:
        return True
    return False

def check_balance_profile(profile: Profile) -> bool:
    """Проверь баланс пользователя и узнай, может он сделать запрос к нейросети или нет"""
    if profile.ai_models_id.code == "mj" and profile.mj_daily_limit - 1 > 0:
        return True
    elif profile.ai_models_id.code == "gpt_4o" and profile.chatgpt_4o_daily_limit - 1 > 0:
        return True
    elif profile.ai_models_id.code == "gpt_4o_mini" and profile.chatgpt_4o_mini_daily_limit - 1 > 0:
        return True
    return False