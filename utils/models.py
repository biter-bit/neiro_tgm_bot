from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import datetime
from sqlalchemy import text, ForeignKey
from typing import Annotated, Optional
from .enum import TariffCode, AiModel


intpk = Annotated[int, mapped_column(primary_key=True)]
created = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated = Annotated[
    datetime.datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow
    )
]                   


class Base(DeclarativeBase):
    pass


class Profile(Base):
    __tablename__ = 'profile'

    id: Mapped[intpk]
    tgid: Mapped[int] = mapped_column(unique=True)
    username: Mapped[Optional[str]] = mapped_column(unique=True)
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    url: Mapped[str | None]
    tariff: Mapped[int | None] = mapped_column(ForeignKey("tariff.id", ondelete='SET NULL'), default=None)
    model: Mapped[AiModel] = mapped_column(default=AiModel.GPT_3_TURBO)
    created_at: Mapped[created]
    updated_at: Mapped[updated]

    # tg_active: Mapped[bool] = mapped_column(default=True)
    # email_confirmed: Mapped[bool] = mapped_column(default=False)
    # avatar: Mapped[str] = mapped_column(default="profile_avatar/default.png")
    #
    # web3id: Mapped[str | None] = mapped_column(unique=True)
    #
    # first_payment: Mapped[bool] = mapped_column(default=True)
    # first_payment_token: Mapped[bool] = mapped_column(default=True)
    # first_payment_api: Mapped[bool] = mapped_column(default=True)
    # recurring: Mapped[bool] = mapped_column(default=True)


class Tariff(Base):
    __tablename__ = 'tariff'

    id: Mapped[intpk]
    name: Mapped[str]
    code: Mapped[TariffCode] = mapped_column(unique=True)
    # description: Mapped[str | None]
    # chatgpt_daily_limit: Mapped[int | None] = mapped_column(default=0)
    # gemini_daily_limit: Mapped[int | None] = mapped_column(default=0)
    # kandinsky_daily_limit: Mapped[int | None] = mapped_column(default=0)
    # sd_daily_limit: Mapped[int | None] = mapped_column(default=0)
    # token_balance: Mapped[int] = mapped_column(default=0)
    # days: Mapped[int] = mapped_column(default=30)
    # price: Mapped[int] = mapped_column(default=0)
    # price_usd: Mapped[float] = mapped_column(default=0)
    # price_ton: Mapped[float] = mapped_column(default=0)
    # price_stars: Mapped[int] = mapped_column(default=0)
    # is_active: Mapped[bool] = mapped_column(default=True)
    # main_tariff: Mapped[int] = mapped_column(ForeignKey('tariff.id'))
    # is_extra: Mapped[bool] = mapped_column(default=False)
    # is_trial: Mapped[bool] = mapped_column(default=False)
    # created_at: Mapped[created]
    # updated_at: Mapped[updated]

#
# profile_table = Table(
#     "profile",
#     metadata_obj,
#     Column("id", Integer, primary_key=True),
#     Column("username", String),
#     Column("email", String),
# )