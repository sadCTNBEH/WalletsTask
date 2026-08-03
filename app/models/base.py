"""Модуль базового класса моделей SQLAlchemy."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Базовый класс для моделей SQLAlchemy."""

    __abstract__ = True
