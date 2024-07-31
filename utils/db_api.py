from sqlalchemy import create_engine
from config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from .models import Base, Profile
from sqlalchemy.future import select

engine_db = create_engine(url=settings.url_connect_with_psycopg2, echo=True)
session_db = sessionmaker(engine_db) # храним обьект сессии для работы с базой в режиме orm
async_engine_db = create_async_engine(url=settings.url_connect_with_asyncpg, echo=True)
async_session_db = async_sessionmaker(async_engine_db)


async def get_or_create_profile(tgid: int, username: str, first_name: str, last_name: str, url: str):
    """Создай пользователя если его нет в бд"""
    async with async_session_db() as session:
        result = await session.execute(select(Profile).filter_by(tgid=tgid))
        profile = result.scalars().first()
        if not profile:
            profile = Profile(username=username, tgid=tgid, first_name=first_name, last_name=last_name)
            session.add(profile)
            await session.commit()
            await session.refresh(profile)
        return profile


def create_tables():
    """Создай таблицы указанные в обьекте metadata"""
    Base.metadata.drop_all(engine_db)
    Base.metadata.create_all(engine_db)