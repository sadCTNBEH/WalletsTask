"""Модуль сервиса для работы с кошельками."""

import uuid
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.wallet import OperationType
from app.models.wallet import Wallet
from app.repository.wallet import WalletRepository
from app.schemas.wallet import WalletResponseModel
from app.service.transaction import commit_transaction


class WalletService:
    """Сервис для выполнения операций с кошельками."""

    def __init__(self, session: AsyncSession) -> None:
        """
        Инициализировать сервис кошельков.

        Args:
            session: Асинхронная сессия базы данных.
        """
        self._session = session
        self._repository = WalletRepository(session)

    async def create_wallet(self) -> Wallet:
        """
        Создать новый кошелёк с нулевым балансом.

        Returns:
            Созданный объект кошелька.
        """

        wallet = await self._repository.create_wallet()
        await commit_transaction(self._session)
        return wallet

    async def get_all_wallets(self) -> list[Wallet]:
        """
        Получить список всех кошельков.

        Returns:
            Список объектов кошельков.
        """

        wallets = await self._repository.get_all_wallets()
        return wallets

    async def get_wallet_balance(self, wallet_uuid: uuid.UUID) -> WalletResponseModel:
        """
        Получить баланс кошелька.

        Args:
            wallet_uuid: Уникальный идентификатор кошелька.

        Returns:
            Текущий баланс кошелька.
        """

        balance = await self._repository.get_wallet_balance(wallet_uuid)
        return WalletResponseModel(id=wallet_uuid, balance=balance)

    async def operation_wallet(
        self, wallet_uuid: uuid.UUID, operation_type: OperationType, amount: Decimal
    ) -> WalletResponseModel:
        """
        Выполнить операцию изменения баланса кошелька.

        Положительная сумма при `DEPOSIT` увеличивает баланс,
        при `WITHDRAW` — уменьшает.

        Args:
            wallet_uuid: Уникальный идентификатор кошелька.
            operation_type: Тип операции (пополнение или снятие).
            amount: Сумма операции.

        Raises:
            WalletNotFound: Если кошелёк не найден.
            InsufficientFundsError: Если недостаточно средств для снятия.
            ValueError: Если передан неизвестный тип операции.
        """

        if amount <= 0:
            raise ValueError("Сумма операции должна быть положительной")

        if operation_type == OperationType.DEPOSIT:
            delta = amount
        elif operation_type == OperationType.WITHDRAW:
            delta = -amount
        else:
            raise ValueError(f"Неизвестный тип операции: {operation_type}")

        result = await self._repository.change_balance(wallet_uuid, delta)
        await commit_transaction(self._session)

        return WalletResponseModel(id=wallet_uuid, balance=result.balance)
