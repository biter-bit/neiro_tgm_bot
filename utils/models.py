from email.policy import default
import uuid

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime
from sqlalchemy import text, ForeignKey, BIGINT, String
from typing import Annotated, Optional
from .enum import TariffCode, AiModel


intpk = Annotated[int, mapped_column(primary_key=True)]
str_50 = Annotated[str, 50]
created = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated = Annotated[
    datetime.datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow
    )
]                   


class Base(DeclarativeBase):
    """Базовый класс моделей."""

    pass


class AiModelCategory(Base):
    """Класс представляет собой класс категорий нейронных сетей."""

    __tablename__ = "ai_model_category"

    id: Mapped[intpk]
    name: Mapped[str | None]
    type: Mapped[str | None]
    description: Mapped[str | None]
    created_at: Mapped[created]
    updated_at: Mapped[updated]


class AiOption(Base):
    """Класс представляет собой доп. настройки для нейронных сетей."""

    __tablename__ = "ai_option"

    id: Mapped[intpk]
    name: Mapped[str | None]
    description: Mapped[str | None]

    # element: Mapped[str | None]
    # values_type: Mapped[str | None]
    # option_type: Mapped[str | None]
    # parameters: Mapped[str | None]
    # defaults: Mapped[str | None]

    created_at: Mapped[created]
    updated_at: Mapped[updated]

    option: Mapped[list["AiModel"]] = relationship(
        back_populates="option",
        secondary="ai_model_option"
    )


class AiModel(Base):
    """Класс представляет из себя модель нейронных сетей"""
    __tablename__ = "ai_model"

    code: Mapped[str | None] = mapped_column(primary_key=True)
    name: Mapped[str | None]
    icon: Mapped[str | None]
    type: Mapped[str | None]
    sequence: Mapped[int | None]
    is_active: Mapped[bool | None]
    cost: Mapped[int | None]
    category_id: Mapped[int | None] = mapped_column(ForeignKey("ai_model_category.id", ondelete='SET NULL'), nullable=True, default=None)
    by_default: Mapped[bool | None]
    description_ru: Mapped[str | None]
    description_ch: Mapped[str | None]
    description_de: Mapped[str | None]
    description_en: Mapped[str | None]
    description_fr: Mapped[str | None]
    description_it: Mapped[str | None]
    description_po: Mapped[str | None]
    description_uk: Mapped[str | None]
    description_us: Mapped[str | None]
    hint_ru: Mapped[str | None]
    hint_ch: Mapped[str | None]
    hint_de: Mapped[str | None]
    hint_en: Mapped[str | None]
    hint_es: Mapped[str | None]
    hint_fr: Mapped[str | None]
    hint_it: Mapped[str | None]
    hint_po: Mapped[str | None]
    hint_uk: Mapped[str | None]
    hint_us: Mapped[str | None]
    created_at: Mapped[created]
    updated_at: Mapped[updated]

    option: Mapped[list["AiOption"]] = relationship(
        back_populates="option",
        secondary="ai_model_option"
    )


class Tariff(Base):
    """Класс представляет собой тариф для пользования нейронными сетями"""
    __tablename__ = "tariff"

    id: Mapped[intpk]
    name: Mapped[str]
    code: Mapped[TariffCode] = mapped_column(unique=True)
    description: Mapped[str | None]
    chatgpt_daily_limit: Mapped[int | None] = mapped_column(default=0)
    gemini_daily_limit: Mapped[int | None] = mapped_column(default=0)
    kandinsky_daily_limit: Mapped[int | None] = mapped_column(default=0)
    sd_daily_limit: Mapped[int | None] = mapped_column(default=0)
    token_balance: Mapped[int] = mapped_column(default=0)
    days: Mapped[int] = mapped_column(default=30)
    price: Mapped[int] = mapped_column(default=0)
    price_usd: Mapped[float] = mapped_column(default=0)
    price_ton: Mapped[float] = mapped_column(default=0)
    price_stars: Mapped[int] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(default=True)

    # main_tariff_id: Mapped[int] = mapped_column(ForeignKey('tariff.id'))
    # is_extra: Mapped[bool] = mapped_column(default=False)

    is_trial: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[created]
    updated_at: Mapped[updated]


class Profile(Base):
    """Класс представляет собой профиль пользователя бота"""
    __tablename__ = "profile"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    tgid: Mapped[int] = mapped_column(BIGINT, unique=True)
    username: Mapped[Optional[str]] = mapped_column(unique=True)
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    email: Mapped[str | None]
    # web3id: Mapped[str | None]
    # tg_active: Mapped[bool] = mapped_column(default=True)
    # email_confirmed: Mapped[bool] = mapped_column(default=False)
    avatar_path: Mapped[str] = mapped_column(default="profile_avatar/default.png")
    url_telegram: Mapped[str | None]
    tariff_id: Mapped[int | None] = mapped_column(ForeignKey("tariff.id", ondelete='SET NULL'),
                                                  nullable=True, default=None)
    ai_model_id: Mapped[int | None] = mapped_column(ForeignKey("ai_model.code", ondelete='SET NULL'),
                                                 nullable=True, default="gpt-4")

    # txt_model: Mapped[AiModel] = mapped_column(ForeignKey("ai_model.code", ondelete='SET NULL'), nullable=True,
    #                                            default=None)
    # img_model: Mapped[AiModel] = mapped_column(ForeignKey("ai_model.code", ondelete='SET NULL'), nullable=True,
    #                                            default=None)

    token_balance: Mapped[Optional[str]]
    update_daily_limits_time: Mapped[Optional[datetime.datetime]]
    chatgpt_daily_limit: Mapped[Optional[int]]
    gemini_daily_limit: Mapped[Optional[int]]
    kandinsky_daily_limit: Mapped[Optional[int]]
    sd_daily_limit: Mapped[Optional[int]]
    language: Mapped[Optional[str]]
    referral_link_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "referral_link.id", ondelete='SET NULL', name="fk_profile_referral_link"
        ),
        nullable=True, default=None
    )
    user_referral_id: Mapped[int | None] = mapped_column(ForeignKey("profile.id", ondelete="SET NULL"),
                                                       nullable=True, default=None)
    # first_payment: Mapped[Optional[bool]]
    # first_payment_token: Mapped[Optional[bool]]
    # first_payment_api: Mapped[Optional[bool]]
    # recurring: Mapped[Optional[bool]]
    # payment_time: Mapped[Optional[datetime.datetime]]
    # payment_tries: Mapped[Optional[int]]

    context_mode: Mapped[Optional[bool]]
    voice_mode: Mapped[Optional[str]]
    txt_model_role_id: Mapped[int | None] = mapped_column(ForeignKey("role.id", ondelete="SET NULL"),
                                                      nullable=True, default=None)
    # api_token: Mapped[Optional[str]]
    # check_subscriptions: Mapped[Optional[bool]]
    # context_participant: Mapped[Optional[bool]]

    finish_training: Mapped[Optional[bool]]
    referral_balance: Mapped[Optional[int]]

    # referral_id: Mapped[Optional[str]]

    created_at: Mapped[created]
    updated_at: Mapped[updated]

    tariffs: Mapped["Tariff"] = relationship()


class Role(Base):
    """Класс представляет собой роль для сценария нейронной сети"""

    __tablename__ = "role"

    id: Mapped[intpk]
    title: Mapped[Optional[str]]
    prompt: Mapped[Optional[str]]
    created_at: Mapped[created]
    updated_at: Mapped[updated]


class ReferralLink(Base):
    """Класс представляет собой реферальную ссылку для пользователя"""

    __tablename__ = "referral_link"

    id: Mapped[intpk]
    name: Mapped[str | None]
    owner: Mapped[int] = mapped_column(ForeignKey("profile.id", ondelete="CASCADE", name="fk_referral_link_owner"))
    clicks: Mapped[Optional[int]]
    buys_cnt: Mapped[Optional[int]]
    new_users: Mapped[Optional[int]]
    enable_landing: Mapped[Optional[bool]]
    bot_link: Mapped[Optional[str]]
    site_link: Mapped[Optional[str]]
    created_at: Mapped[created]
    updated_at: Mapped[updated]


class AiModelOptionM2M(Base):
    """Класс представляет себя связующую таблицу опций модели и саму модель"""

    __tablename__ = "ai_model_option"

    id: Mapped[intpk]
    ai_model_id: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("ai_model.code", ondelete="CASCADE"),
        primary_key=True
    )
    ai_option_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("ai_option.id", ondelete="CASCADE"),
        primary_key=True
    )


class ChatSession(Base):
    """Класс представляет себя сессию чата (историю переписки с моделью)"""

    __tablename__ = "chat_session"

    id: Mapped[intpk]
    name: Mapped[str]
    ai_model_id: Mapped[int | None] = mapped_column(ForeignKey("ai_model.code", ondelete="CASCADE"),
                                                   nullable=True, default=None)
    profile_id: Mapped[int | None] = mapped_column(ForeignKey("profile.id", ondelete="CASCADE"),
                                                  nullable=True, default=None)
    active_generation: Mapped[Optional[bool]]
    anonymous_chat: Mapped[Optional[bool]]
    folder_id: Mapped[int | None] = mapped_column(ForeignKey("chat_folder.id", ondelete="SET NULL"),
                                                    nullable=True, default=None)

    # main_session_id: Mapped["ChatSession"] = mapped_column(ForeignKey("chat_session.id", ondelete='SET NULL'))

    pinned: Mapped[Optional[bool]]
    int: Mapped[Optional[int]]
    created_at: Mapped[created]
    updated_at: Mapped[updated]


class ChatFolder(Base):
    """Класс представляет себя папку сессий пользователя"""

    __tablename__ = "chat_folder"

    id: Mapped[intpk]
    name: Mapped[Optional[str]]
    profile_id: Mapped[int | None] = mapped_column(ForeignKey("profile.id", ondelete="CASCADE"),
                                                  nullable=True, default=None)
    pinned: Mapped[Optional[bool]]
    position: Mapped[Optional[int]]
    created_at: Mapped[created]
    updated_at: Mapped[updated]


class TextQuery(Base):
    """Класс представляет себя запрос, отправленный к текстовой модели и от нее"""

    __tablename__ = "text_query"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    chat_session_id: Mapped[uuid.UUID] = mapped_column(nullable=True)
    query: Mapped[Optional[str]] = mapped_column(nullable=True)
    answer: Mapped[Optional[str]] = mapped_column(nullable=True)
    from_group: Mapped[Optional[bool]] = mapped_column(nullable=False)
    status: Mapped[Optional[str]] = mapped_column(nullable=False)

    created_at: Mapped[created]
    updated_at: Mapped[updated]


class ImageQuery(Base):
    """Класс представляет себя запрос, отправленный к модели генерации картинки и от нее"""

    __tablename__ = "image_query"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    chat_session_id: Mapped[uuid.UUID] = mapped_column(nullable=True)
    query: Mapped[Optional[str]] = mapped_column(nullable=True)
    # index: Mapped[Optional[int]]
    type_query: Mapped[Optional[str]] = mapped_column(nullable=False)
    result: Mapped[Optional[str]] = mapped_column(nullable=True)
    task_number: Mapped[uuid.UUID] = mapped_column(nullable=True)
    from_group: Mapped[Optional[bool]] = mapped_column(nullable=False)
    status: Mapped[Optional[str]] = mapped_column(nullable=False)


    created_at: Mapped[created]
    updated_at: Mapped[updated]


class VideoQuery(Base):
    """Класс представляет себя запрос, отправленный к видео модели и от нее"""

    __tablename__ = "video_query"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    chat_session_id: Mapped[uuid.UUID] = mapped_column(nullable=True)
    query: Mapped[Optional[str]] = mapped_column(nullable=True)
    result: Mapped[Optional[str]] = mapped_column(nullable=True)
    task_number: Mapped[uuid.UUID] = mapped_column(nullable=True)
    from_group: Mapped[Optional[bool]] = mapped_column(nullable=False)
    status: Mapped[Optional[str]] = mapped_column(nullable=False)

    created_at: Mapped[created]
    updated_at: Mapped[updated]