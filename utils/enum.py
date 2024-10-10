from enum import Enum
import textwrap
import locale
from datetime import datetime, timedelta


class NameButtons(Enum):
    """Класс с названиями кнопок"""
    START = "Главное меню"

    @classmethod
    def get_list_value(cls):
        result = []
        for i in cls:
            result.append(i.value)
        return result

class Messages(Enum):
    """Класс с сообщениями для пользователей"""
    START = textwrap.dedent(
        """
        Это бот ChatGPT + MidJourney в Telegram. 
        По умолчанию выбрана нейросеть ChatGPT. Просто выберите нужную нейросеть или сразу напишите ваш запрос.
        
        Команды
        /start - перезапуск
        /mode - выбрать нейросеть
        /profile - профиль пользователя
        /pay - купить подписку
        /reset - сброс контекста
        /help - помощь
        /ask - задать вопрос (в группах)
        """
    )

    _PROFILE_FREE = textwrap.dedent(
        """
        👤 Мой профиль
        
        ID: {tgid}
        Подписка: {code_tariff}
        Чтобы добавить подписку нажмите /pay
        
        👾 Лимиты
        GPT-4o mini — БЕЗЛИМИТ
        GPT-4o - доступен только по подписке (/pay)
        Midjourney v5.2 - доступен только по подписке (/pay)
        Midjourney v6.0 - доступен только по подписке (/pay)
        """
    )

    _PROFILE_NOT_FREE = textwrap.dedent(
        """
        👤 Мой профиль
        
        ID: {tgid}
        Подписка: {code_tariff}
        Чтобы добавить подписку нажмите /pay
    
        👾 Лимиты
        GPT-4o mini — БЕЗЛИМИТ
        GPT-4o - {available_chatgpt_4o}/{limit_chatgpt_4o} (/pay)
        Midjourney v5.2 - {available_mj_5_2}/{limit_mj_5_2} (/pay)
        Midjourney v6.0 - {available_mj_6_0}/{limit_mj_6_0} (/pay)
        
        🔄 Обновление лимитов: {update_limit}
        """
    )

    RESET = textwrap.dedent(
        """
        Контекст успешно удален!
        """
    )

    HELP = textwrap.dedent(
        """
        📚 О боте
        
        Бот работает через официальный API ChatGPT от OpenAI последней версии. Мы предоставляем 30 запросов бесплатно. Они обновляются каждую неделю. 
        
        Чтобы использовать бота без ограничений, вы можете приобрести подписку по команде /pay.
        
        1. Что такое контекст?
        По умолчанию бот работает в режиме контекста, то есть запоминает предыдущие сообщения. Это сделано для того, чтобы можно было уточнить дополнения или вести диалог в рамках одной темы. Команда /reset сбрасывает контекст.
        
        2. Распознавание изображений
        ChatGPT-4o умеет распознавать изображения. Для этого прикрепите изображение к запросу.
        
        3. Генерация изображений
        – Чтобы обратиться к Midjourney, отправьте команду и текст сообщения: «/img текст запроса».
        – Чтобы сгенерировать изображение на основе другого изображения, прикрепите его к вашему запросу или вставьте ссылку на изображение.
        – Генерация доступна на русском и английском языках.
        
        4. Лимиты и подписка
        Чтобы поддерживать стабильную работу без перегрузок, мы должны использовать лимиты на генерацию. Сейчас лимиты такие:
        
        🪫 Бесплатно:
        • GPT-4o mini – БЕЗЛИМИТ.
        
        🔋 В подписке Plus:
        • GPT-4o mini – БЕЗЛИМИТ.
        • GPT-4o – 100 запросов в день
        • o1-preview – 20 запросов в день
        • o1-mini – 60 запросов в день
        • GPT-4 Vision (распознавание изображений)
        • Midjourney v5.2 – 45 запросов в день
        • Midjourney v6.0 – 20 запросов в день
        
        Вы можете управлять подпиской в разделе /profile.
        
        5. Поддержка пользователей
        Если у вас возникли какие-то вопросы, вы всегда можете написать в поддержку: @Neyrosetka_com. Режим работы: 08:00 - 23:00 по мск.
        """
    )

    PAY = textwrap.dedent(
        """
        Подписка ⚡️Plus:

        - GPT-4o mini — безлимитно;
        - GPT-4o — 100 запросов в день;
        - o1-preview — 20 запросов в день;
        - o1-mini — 60 запросов в день;
        - GPT-4 Vision (Распознавание изображений);
        - Midjourney v5.2 — 45 запросов в день;
        - Midjourney v6.0 — 20 запросов в день.
        
        Стоимость: 489р в месяц
        """
    )

    CHOICE_MODE = textwrap.dedent(
        """
        🤖 Выберите модели нейросетей:
        
        1. ChatGPT-4o
        Основная модель с высоким интеллектом. Оптимальна для большинства задач. 
        
        2. ChatGPT-4o mini
        Доступная небольшая модель для быстрых и простых задач. 
        
        3. o1-preview 
        Ранняя версия, предназначенная для решения сложных задач с использованием широких общих знаний.
        
        4. o1-mini
        Более быстрая и экономически эффективная версия, особенно подходящая для задач программирования, математики и науки, которые не требуют обширных общих знаний.          
        """
    )

    CHOICE = textwrap.dedent(
        """
        Модель {model_name} выбрана!
        """
    )

    ERROR = textwrap.dedent(
        """
        🤖 Похоже у создателей этой нейросети возникли проблемы, мы вместе с Вами ждем пока восстановится доступ, 
        попробуйте ваш запрос позже или воспользуйтесь другой нейросетью или сервисом.

        * Ваши токены не были потрачены,  тк запрос в  нейросеть не прошел.
        """
    )

    @classmethod
    def create_message_choice_model(cls, model_name: str):
        return cls.CHOICE.value.format(
            model_name=model_name
        )

    @staticmethod
    def format_date(dt: datetime) -> str:
        """Верни дату в нужном формате

        Пример: 'среда, 11 сентября 2024 г. в 15:20 (мск)'
        """
        dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        formating_date = dt.strftime('%A, %d %B %Y г. в %H:%M')
        formating_date = formating_date.lower().replace(" 0", " ")
        formating_date += ' (мск)'
        return formating_date

    @classmethod
    def create_message_profile(cls, profile):
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        formating_date = cls.format_date(datetime.now() + timedelta(days=1))
        if profile.tariffs.name == 'Free':
            return cls._PROFILE_FREE.value.format(
                tgid=profile.tgid,
                code_tariff=profile.tariffs.name,
            )
        else:
            return cls._PROFILE_NOT_FREE.value.format(
                tgid=profile.tgid,
                code_tariff=profile.tariffs.name,
                available_chatgpt_4o=profile.chatgpt_4o_daily_limit,
                limit_chatgpt_4o=profile.tariffs.chatgpt_4o_daily_limit,
                available_mj_5_2=profile.mj_daily_limit_5_2,
                limit_mj_5_2=profile.tariffs.midjourney_5_2_daily_limit,
                available_mj_6_0=profile.mj_daily_limit_6_0,
                limit_mj_6_0=profile.tariffs.midjourney_6_0_daily_limit,
                update_limit=formating_date,
            )


class MjOption(Enum):
    """Класс со способами запросов к mj api"""
    VARIATION = 'variation'
    UPSAMPLE = 'upsample'

class PaymentName(Enum):
    """Класс со способами оплаты"""
    STARS = "stars"
    ROBOKASSA = "robokassa"

class Errors(Enum):
    """Класс с ошибками"""
    ERROR_ACTIVE_GENERATE = 'You have already activated generation. Wait for it to complete.'
    ERROR_BALANCE_FREE = "Top up your balance. Available to you {limit_current_model} generations."
    ERROR_BALANCE_PAID = "Top up your balance."
    ERROR_TARIFF = "Model {} is not available for tariff {}"
    NON_ERROR = "Ok"

    @classmethod
    def error_balance_free(cls, limit_current_model: str):
        return cls.ERROR_BALANCE_FREE.value.format(limit_current_model)

    @classmethod
    def error_tariff(cls, ai_model_id: str, tariff_name: str):
        return cls.ERROR_TARIFF.value.format(ai_model_id, tariff_name)

class AiModelName(Enum):
    """Класс с названиями нейросетей"""
    GPT_4_O = "gpt-4o"
    GPT_4_O_MINI = "gpt-4o-mini"
    MIDJOURNEY_6_0 = "mj-6-0"
    MIDJOURNEY_5_2 = "mj-5-2"
    GPT_O1_PREVIEW = "o1-preview"
    GPT_O1_MINI = "o1-mini"

    @classmethod
    def get_list_value(cls):
        result = []
        for i in cls:
            result.append(i.value)
        return result

    @classmethod
    def get_need_format(cls, model):
        result = ''
        if model == cls.GPT_4_O.value:
            result = 'GPT-4o'
        elif model == cls.GPT_4_O_MINI.value:
            result = 'GPT-4o-mini'
        elif model == cls.MIDJOURNEY_5_2.value:
            result = 'Midjourney 6.0'
        elif model == cls.MIDJOURNEY_6_0.value:
            result = 'Midjourney 5.2'
        elif model == cls.GPT_O1_PREVIEW.value:
            result = 'o1-preview'
        elif model == cls.GPT_O1_MINI.value:
            result = 'o1-mini'
        return result

    @classmethod
    def get_enum_field_by_value(cls, value: str):
        for field in cls:
            if field.value == value:
                return field
        return None


class TariffCode(Enum):
    """Класс с названиями тариффов"""
    FREE = "Free"
    PREMIUM = "premium"
