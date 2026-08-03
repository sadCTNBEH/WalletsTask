"""Модуль настройки подключения к базе данных."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

engine = create_async_engine(
    "postgresql+asyncpg://postgres_user:postgres_password@db:5432/postgres_db"
)

SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Получить асинхронную сессию базы данных.

    Создает новую сессию SQLAlchemy для обработки запроса
    и выполняет откат транзакции в случае ошибки.

    Yields:
        AsyncSession: Асинхронная сессия базы данных.
    """

    async with SessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
