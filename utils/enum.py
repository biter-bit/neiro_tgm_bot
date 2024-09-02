from enum import Enum


class MainButton(Enum):
    """Класс с названиями кнопок"""
    START = "Перезапуск бота"


class Messages(Enum):
    """Класс с сообщениями для пользователей"""
    START = '''
Это бот ChatGPT + MidJourney в Telegram. 
По умолчанию выбрана нейросеть ChatGPT. Просто выберите нужную нейросеть или сразу напишите ваш запрос.

Команды
/start - перезапуск
/profile - профиль пользователя
/pay - купить подписку
/reset - сброс контекста
/help - помощь
/ask - задать вопрос (в группах)
    
Подпишитесь на наш Telegram канал про технологии: @naebnet (https://t.me/+-P-yDHu8BuEyODIy)
    '''

    PROFILE = '''
    Это ваш профиль.
    ID: {tgid}
    Подписка: {code_tariff}
    Чтобы добавить подписку нажмите /pay
    
    Лимиты
    GPT-4o mini — осталось {limit}/30
    Обновление лимитов: {update_limit} (мск)
    '''

    @classmethod
    def create_message_profile(cls, profile):
        return cls.PROFILE.value.format(
            tgid=profile.tgid,
            code_tariff=profile.tariffs.code.value,
            limit=profile.chatgpt_daily_limit,
            update_limit=profile.update_daily_limits_time
        )


class AiModel(Enum):
    """Класс с названиями нейросетей"""
    GPT_3_TURBO = "gpt-3.5-turbo-1106"
    GPT_4 = "gpt-4"
    GPT_4_TURBO = "gpt-4-1106-preview"
    GPT_4_VISION = "gpt-4-vision-preview"
    GPT_4_O = "gpt-4o"
    STABLE_DIFFUSION = "sd"
    MIDJORNEY = "mj"
    DALLE_2 = "dall-e-2"
    DALLE_3 = "dall-e-3"
    YAGPT_LITE = "yandexgpt-lite"
    YAGPT = "yandexgpt"
    KANDINSKY = "kandinsky"
    BARD = "bard"
    CLAUDE_OPUS = "claude-3-opus-20240229"
    CLAUDE_SONNET = "claude-3-sonnet-20240229"
    CLAUDE_HAIKU = "claude-3-haiku-20240307"
    PICA = "pica"

    @classmethod
    def get_enum_field_by_value(cls, value: str):
        for field in cls:
            if field.value == value:
                return field
        return None


class TariffCode(Enum):
    """Класс с названиями тариффов"""
    FREE = "free"
    TRIAL_50 = "trial_50"
    TRIAL_500 = "trial_500"
    MAIN_500 = "main_500"
    TRIAL_1500 = "trial_1500"
    MAIN_1500 = "main_1500"
    TRIAL_3000 = "trial_3000"
    MAIN_3000 = "main_3000"
    TRIAL_6000 = "trial_6000"
    MAIN_6000 = "main_6000"
    TOKEN_300 = "token_300"
    TOKEN_450 = "token_450"
    TOKEN_3000 = "token_3000"
    TOKEN_9000 = "token_9000"
    API_1000 = "api_1000"
    API_5000 = "api_5000"
    API_10000 = "api_10000"
    API_25000 = "api_25000"
    API_50000 = "api_50000"
