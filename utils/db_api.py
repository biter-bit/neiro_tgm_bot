from cgitb import reset

from sqlalchemy import create_engine, text
from config import settings
from sqlalchemy.orm import sessionmaker, joinedload, selectinload
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from services import chat_gpt
from .models import Base, Profile, AiModel, ChatSession, TextQuery, Tariff
from sqlalchemy.future import select
import subprocess

engine_db = create_engine(url=settings.url_connect_with_psycopg2, echo=True) # движок для работы с orm (psycopg2)
session_db = sessionmaker(engine_db) # обьект сессии для работы с базой в режиме orm
async_engine_db = create_async_engine(url=settings.url_connect_with_asyncpg, echo=True)
async_session_db = async_sessionmaker(async_engine_db)


async def save_message(answer: str, text_query_id):
    """Сохрани ответ текстовой нейронки в бд"""
    async with async_session_db() as session:
        text_query = await session.get(TextQuery, text_query_id)
        text_query.answer = answer
        text_query.status = 'finish'
        await session.commit()
        return text_query


async def create_text_query(query: str, chat_session_id):
    """Подготовь текстовый запрос"""
    async with async_session_db() as session:
        text_query = TextQuery(
            status="in_process",
            query=query,
            chat_session_id=chat_session_id,
            from_group=False
        )
        session.add(text_query)
        await session.commit()
        await session.refresh(text_query)
        return text_query

async def get_text_messages_from_session(session_id: int, name_ai_model: str):
    """Верни список сообщений с нейронной сетью в сессии"""
    async with async_session_db() as session:
        messages = []
        query = (
            select(ChatSession)
            .filter_by(id=session_id, ai_model_id=name_ai_model)
            .options(selectinload(ChatSession.text_queries))
        )
        result = await session.execute(query)
        session_chat = result.unique().scalars().first()
        for msg in session_chat.text_queries:
            if msg.query and msg.answer:
                messages.append({"role": "user", "content": msg.query})
                messages.append({"role": "assistant", "content": msg.answer})
        return messages

async def replace_model_of_profile(profile: Profile, model: str):
    """Измени модель для пользователя"""
    async with async_session_db() as session:
        profile_obj = await session.get(Profile, profile.id)
        profile_obj.ai_model_id = model
        await session.commit()
        await session.refresh(profile_obj)
        return profile_obj

async def delete_context_from_session(session_id: int, profile: Profile) -> str:
    """Удали выбранную сессию и создай новую"""
    async with async_session_db() as session:
        session_obj = await session.get(ChatSession, session_id)
        if not session_obj:
            return "Not object"
        await session.delete(session_obj)
        await session.commit()
    await get_or_create_session(profile, profile.ai_model_id)
    return "Ok"

async def get_or_create_session(profile: Profile, model: str):
    """Создай сессию для пользователя если ее нет"""
    async with async_session_db() as session:
        query = (
            select(ChatSession)
            .filter_by(profile_id=profile.id, ai_model_id=model)
            .options(selectinload(ChatSession.text_queries))
            .options(selectinload(ChatSession.image_queries))
            .options(selectinload(ChatSession.video_queries))
        )
        result = await session.execute(query)
        session_chat = result.unique().scalars().first()
        if not session_chat:
            session_chat = ChatSession(
                profile_id=profile.id,
                ai_model_id=model,
                name='Новый диалог 1',
            )
            session.add(session_chat)
            await session.commit()
            await session.refresh(session_chat)
        return session_chat

async def active_generic_in_session(chat_session_id: int):
    """Включи статус генерации в указанной сессии"""
    async with async_session_db() as session:
        chat_session = await session.get(ChatSession, chat_session_id)
        chat_session.active_generation = True
        await session.commit()
        return "Ok"

async def deactivate_generic_in_session(chat_session_id: int):
    """Выключи статус генерации в указанной сессии"""
    async with async_session_db() as session:
        chat_session = await session.get(ChatSession, chat_session_id)
        chat_session.active_generation = False
        await session.commit()
        return "Ok"

async def subtracting_tokens_from_profile_balance(profile_id: int, deductible_token: int) -> str:
    """Удали кол-во токенов запроса"""
    async with async_session_db() as session:
        profile_obj = await session.get(Profile, profile_id)
        profile_obj.token_balance -= deductible_token
        await session.commit()
        return "Ok"

async def subtracting_count_request_to_model_chatgpt_4o_mini(profile_id: int) -> str:
    """Вычти кол-во допустимых запросов к модели chatgpt_4o_mini на 1 для пользователя."""
    async with async_session_db() as session:
        profile_id = await session.get(Profile, profile_id)
        profile_id.chatgpt_daily_limit -= 1
        await session.commit()
        return "Ok"

async def get_or_create_profile(tgid: int, username: str, first_name: str, last_name: str, url: str):
    """Создай пользователя если его нет в бд"""
    async with async_session_db() as session:
        query = (
            select(Profile)
            .filter_by(tgid=tgid)
            .options(joinedload(Profile.tariffs))
            .options(joinedload(Profile.ai_models_id))
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

async def get_tariff(tariff_id):
    """Получи тариф"""
    async with async_session_db() as session:
        tariff_obj = await session.get(Tariff, tariff_id)
        return tariff_obj

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
