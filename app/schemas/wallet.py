"""Модуль схем Pydantic для работы с кошельками."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.enums.wallet import OperationType


class OperationWallet(BaseModel):
    """Схема операции изменения баланса кошелька."""

    operation_type: OperationType
    amount: Decimal = Field(gt=0)


class CreateWalletResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    balance: Decimal
    created_at: datetime
    updated_at: datetime


class WalletResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    balance: Decimal
