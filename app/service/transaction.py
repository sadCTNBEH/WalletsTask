"""Модуль вспомогательных функций для работы с транзакциями базы данных."""

from sqlalchemy.ext.asyncio import AsyncSession


async def commit_transaction(session: AsyncSession) -> None:
    """
    Зафиксировать изменения в базе данных.

    Выполняет commit текущей транзакции.
    В случае ошибки выполняет откат транзакции.

    Args:
        session: Асинхронная сессия базы данных.

    Raises:
        Exception: Пробрасывает исключение, возникшее при фиксации транзакции.
    """

    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise
