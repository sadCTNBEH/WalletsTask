"""Модуль ORM-модели кошелька."""

import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Numeric, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7

from app.models.base import Base


class Wallet(Base):
    """
    Модель кошелька пользователя.

    Содержит идентификатор, текущий баланс и
    временные метки создания и обновления записи.
    """

    __tablename__ = "wallet"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid7)
    balance: Mapped[Decimal] = mapped_column(
        Numeric(precision=20, scale=2), nullable=False, default=Decimal(0)
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
