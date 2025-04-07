from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool  # Пул соединений для production

from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

# Формат: postgresql+asyncpg://<пользователь>:<пароль>@<хост>:<порт>/<имя_базы>
DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Создаём асинхронный движок для SQLAlchemy
# Этот движок будет использоваться для подключения к PostgreSQL
engine = create_async_engine(DATABASE_URL, poolclass=NullPool)

# Базовый класс для ORM-моделей
# Каждая модель таблицы будет наследоваться от этого класса
Base = declarative_base()


# Фабрика асинхронных сессий
# Позволяет создавать объекты типа AsyncSession для выполнения SQL-запросов
# expire_on_commit=False позволяет использовать объекты после коммита (без ошибки DetachedInstanceError)

async_session_maker = sessionmaker(
    bind=engine,  # Привязываем к нашему движку
    class_=AsyncSession,  # Асинхронные сессии
    expire_on_commit=False  # Не очищать объекты после коммита
)


# Асинхронная зависимость для FastAPI
# Используется внутри эндпоинтов для автоматического подключения сессии БД
# FastAPI будет сам вызывать эту функцию при запросе
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    # Контекстный менеджер async with гарантирует, что сессия будет автоматически закрыта после работы
    async with async_session_maker() as session:
        # Возвращаем сессию наружу — FastAPI получит её и сможет выполнить SQL-запросы
        yield session