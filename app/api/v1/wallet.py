"""API-эндпоинты для работы с кошельками."""

import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.schemas.wallet import (
    CreateWalletResponse,
    OperationWallet,
    WalletResponseModel,
)
from app.service.wallet import WalletService

router = APIRouter()


@router.post(
    "/wallet",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateWalletResponse,
)
async def create_wallet(session: AsyncSession = Depends(get_session)):
    wallet_service = WalletService(session)
    return await wallet_service.create_wallet()


@router.get("/wallet")
async def get_wallets(session: AsyncSession = Depends(get_session)):
    wallet_service = WalletService(session)
    return await wallet_service.get_all_wallets()


@router.get(
    "/wallet/{wallet_uuid}",
    status_code=status.HTTP_200_OK,
    response_model=WalletResponseModel,
)
async def get_wallet_balance(
    wallet_uuid: uuid.UUID, session: AsyncSession = Depends(get_session)
):
    """
    Получить баланс кошелька по его идентификатору.

    Args:
        wallet_uuid: Уникальный идентификатор кошелька.
        session: Асинхронная сессия базы данных.

    Returns:
        Текущий баланс кошелька.

    Raises:
        WalletNotFound: Если кошелек не найден.
    """

    wallet_service = WalletService(session)
    return await wallet_service.get_wallet_balance(wallet_uuid)


@router.post(
    "/wallet/{wallet_uuid}/operation",
    status_code=status.HTTP_200_OK,
    response_model=WalletResponseModel,
)
async def operation_wallet(
    wallet_uuid: uuid.UUID,
    operation: OperationWallet,
    session: AsyncSession = Depends(get_session),
):
    """
    Выполнить операцию изменения баланса кошелька.

    Поддерживаемые типы операций (Enum `OperationType`):
    - DEPOSIT - пополнение баланса
    - WITHDRAW - снятие средств

    Args:
        wallet_uuid: Уникальный идентификатор кошелька.
        operation: Тип операции и сумма изменения баланса.
        session: Асинхронная сессия базы данных.

    Returns:
        Результат выполнения операции.

    Raises:
        WalletNotFound: Если кошелек не найден.
        InsufficientFundsError: Если недостаточно средств для снятия.
    """

    wallet_service = WalletService(session)
    return await wallet_service.operation_wallet(
        wallet_uuid, operation.operation_type, operation.amount
    )
