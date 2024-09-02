from sqlalchemy import create_engine, text
from config import settings
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from .models import Base, Profile, AiModel
from sqlalchemy.future import select
import subprocess

engine_db = create_engine(url=settings.url_connect_with_psycopg2, echo=True) # движок для работы с orm (psycopg2)
session_db = sessionmaker(engine_db) # обьект сессии для работы с базой в режиме orm
async_engine_db = create_async_engine(url=settings.url_connect_with_asyncpg, echo=True)
async_session_db = async_sessionmaker(async_engine_db)


async def get_or_create_profile(tgid: int, username: str, first_name: str, last_name: str, url: str):
    """Создай пользователя если его нет в бд"""
    async with async_session_db() as session:
        query = (
            select(Profile)
            .filter_by(tgid=tgid)
            .options(joinedload(Profile.tariffs))
        )
        result = await session.execute(query)
        profile = result.unique().scalars().first()
        if not profile:
            profile = Profile(
                username=username,
                tgid=tgid,
                first_name=first_name,
                last_name=last_name,
                url_telegram=url,
                avatar_path=f"{settings.PATH_WORK}/images/profiles/default.jpg",
                tariff_id=1
            )
            session.add(profile)
            await session.commit()
            await session.refresh(profile)
        return profile


async def get_all_ai_models() -> dict:
    """Получи все модели нейронок из бд в виде словаря"""
    async with async_session_db() as session:
        result = await session.execute(select(AiModel))
        ai_models = result.scalars().all()
        ai_models_dict = {model.code: model for model in ai_models}
    return ai_models_dict


def create_tables():
    """Создай таблицы указанные в обьекте metadata"""
    Base.metadata.drop_all(engine_db)
    Base.metadata.create_all(engine_db)
    subprocess.run([f"{settings.PATH_WORK}/bash.sh"], capture_output=True, text=True)
