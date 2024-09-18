from enum import Enum
import textwrap
import locale
from datetime import datetime


class NameButtons(Enum):
    """Класс с названиями кнопок"""
    START = "Главное меню"


class Messages(Enum):
    """Класс с сообщениями для пользователей"""
    START = textwrap.dedent(
        """
        Это бот ChatGPT + MidJourney в Telegram. 
        По умолчанию выбрана нейросеть ChatGPT. Просто выберите нужную нейросеть или сразу напишите ваш запрос.
        
        Команды
        /start - перезапуск
        /profile - профиль пользователя
        /pay - купить подписку
        /reset - сброс контекста
        /help - помощь
        /ask - задать вопрос (в группах)
        """
    )

    _PROFILE_FREE = textwrap.dedent(
        """
        Это ваш профиль.
        ID: {tgid}
        Подписка: {code_tariff}
        Чтобы добавить подписку нажмите /pay
        
        Лимиты
        GPT-4o mini — осталось {available}/{limit}
        GPT-4o - доступен только по подписке (/pay)
        Midjourney - доступен только по подписке (/pay)
        
        Обновление лимитов: {update_limit}
        """
    )

    _PROFILE_NOT_FREE = textwrap.dedent(
        """
        Это ваш профиль.
        ID: {tgid}
        Подписка: {code_tariff}
        Чтобы добавить подписку нажмите /pay
    
        Лимиты
        Доступны все нейросети без ограничений!
        """
    )

    RESET = textwrap.dedent(
        """
        Контекст успешно удален!
        """
    )

    HELP = textwrap.dedent(
        """
        О боте
        Бот работает через официальный API ChatGPT от OpenAI последней версии.
        
        Мы предоставляем 30 запросов бесплатно. Они обновляются каждую неделю. Чтобы использовать бота без ограничений, вы можете приобрести подписку по команде /pay
        
        Что такое контекст?
        По умолчанию бот работает в режиме контекста, то есть запоминает предыдущие сообщения. Это сделано для того, чтобы можно было уточнить дополнения или вести диалог в рамках одной темы. Команда /reset сбрасывает контекст.
        
        Распознавание изображений
        GPT-4o умеет распознавать изображения. Для этого прикрепите изображение к запросу.
        
        Генерация изображений
        - Чтобы обратиться к Midjourney, отправьте команду и текст сообщения: «/img текст запроса».
        - Чтобы сгенерировать изображение на основе другого изображения, прикрепите его к вашему запросу или вставьте ссылку на изображение.
        - Генерация доступна на русском и английском языках.
        
        Лимиты и подписка
        Чтобы поддерживать стабильную работу без перегрузок, мы должны использовать лимиты на генерацию. Сейчас лимиты такие:
        
        Бесплатно:
        - GPT-4o mini — 30 запросов в неделю;
        
        ⚡️В подписке Plus:
        - GPT-4o mini — безлимитно;
        - GPT-4o — 50 запросов в день;
        - GPT-4o Vision (Распознавание изображений);
        - Midjorney v5.2 — 25 запросов в день;
        - Midjorney v6.0 — 10 запросов в день.
        
        Вы можете управлять подпиской в разделе /profile.
        
        Поддержка пользователей
        Написать в поддержку — @gpts_support. Режим работы: 08:00 - 23:00 по мск.
        """
    )

    PAY = textwrap.dedent(
        """
        Подписка ⚡️Plus:

        - GPT-4o mini — безлимитно;
        - GPT-4o — 50 запросов в день; 
        - Midjourney v6.1 — 10 запросов в день.
        Стоимость: 499р / за 30д
        """
    )

    CHOICE = textwrap.dedent(
        """
        Модель {model_name} выбрана!
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
        formating_date = dt.strftime('%A, %d %B %Y г. в %H:%M')
        formating_date = formating_date.lower().replace(" 0", " ")
        formating_date += ' (мск)'
        return formating_date

    @classmethod
    def create_message_profile(cls, profile):
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        formating_date = cls.format_date(profile.update_daily_limits_time)
        if profile.tariffs.name == 'Free':
            return cls._PROFILE_FREE.value.format(
                tgid=profile.tgid,
                code_tariff=profile.tariffs.code.value,
                available=profile.chatgpt_4o_mini_daily_limit,
                limit=profile.tariffs.chatgpt_4o_mini_daily_limit,
                update_limit=formating_date,
            )
        else:
            return cls._PROFILE_NOT_FREE.value.format(
                tgid=profile.tgid,
                code_tariff=profile.tariffs.code.value,
            )


class MjOption(Enum):
    """Класс со способами запросов к mj api"""
    VARIATION = 'variation'
    UPSAMPLE = 'upsample'

class Errors(Enum):
    """Класс с ошибками"""

class AiModelName(Enum):
    """Класс с названиями нейросетей"""
    GPT_4_O = "gpt-4o"
    GPT_4_O_MINI = "gpt-4o-mini"
    MIDJOURNEY = "mj"

    @classmethod
    def get_enum_field_by_value(cls, value: str):
        for field in cls:
            if field.value == value:
                return field
        return None


class TariffCode(Enum):
    """Класс с названиями тариффов"""
    FREE = "free"
    PREMIUM = "premium"
