"""Модуль репозитория кошельков."""

import uuid
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.wallet import InsufficientFundsError, WalletNotFound
from app.models.wallet import Wallet


class WalletRepository:
    """Репозиторий для работы с кошельками."""

    def __init__(self, session: AsyncSession) -> None:
        """
        Инициализировать репозиторий кошельков.

        Args:
            session: Асинхронная сессия базы данных.
        """

        self._session = session

    async def _get_wallet_for_update(self, wallet_uuid: uuid.UUID) -> Wallet:
        """
        Получить кошелёк с блокировкой строки.

        Используется при изменении баланса, чтобы избежать гонок.

        Args:
            wallet_uuid: Уникальный идентификатор кошелька.

        Returns:
            Объект кошелька.

        Raises:
            WalletNotFound: Если кошелёк не найден.
        """

        stmt = select(Wallet).where(Wallet.id == wallet_uuid).with_for_update()
        result = await self._session.execute(stmt)
        wallet = result.scalar_one_or_none()

        if wallet is None:
            raise WalletNotFound(f"Кошелек {wallet_uuid} не найден")

        return wallet

    async def create_wallet(self) -> Wallet:
        """
        Создать новый кошелёк с нулевым балансом.

        Returns:
            Созданный объект кошелька.
        """

        wallet = Wallet(balance=Decimal(0))
        self._session.add(wallet)
        await self._session.flush()
        await self._session.refresh(wallet)

        return wallet

    async def get_all_wallets(self) -> list[Wallet]:
        """
        Получить список всех кошельков.

        Returns:
            Список объектов кошельков.
        """

        stmt = select(Wallet)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get_wallet_balance(self, wallet_uuid: uuid.UUID) -> Decimal:
        """
        Получить баланс кошелька.

        Args:
            wallet_uuid: Уникальный идентификатор кошелька.

        Returns:
            Текущий баланс кошелька.

        Raises:
            WalletNotFound: Если кошелек не найден.
        """

        stmt = select(Wallet.balance).where(Wallet.id == wallet_uuid)
        result = await self._session.scalar(stmt)

        if result is None:
            raise WalletNotFound()
        return result

    async def change_balance(
        self,
        wallet_uuid: uuid.UUID,
        amount: Decimal,
    ) -> Wallet:
        """
        Изменить баланс кошелька на указанную сумму.

        Положительное значение `amount` - пополнение,
        отрицательное - снятие.

        Args:
            wallet_uuid: Уникальный идентификатор кошелька.
            amount: Сумма изменения баланса.

        Raises:
            WalletNotFound: Если кошелёк не найден.
            InsufficientFundsError: Если после операции баланс стал бы отрицательным.
        """

        wallet = await self._get_wallet_for_update(wallet_uuid)
        new_balance = wallet.balance + amount
        if new_balance < 0:
            raise InsufficientFundsError("Недостаточно средств")
        wallet.balance = new_balance
        await self._session.flush()
        return wallet
