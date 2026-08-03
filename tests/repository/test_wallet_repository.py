import uuid
from decimal import Decimal

import pytest
from hamcrest import assert_that, equal_to
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.wallet import InsufficientFundsError, WalletNotFound
from app.repository.wallet import WalletRepository


@pytest.mark.asyncio
async def test_get_wallet_balance_success(db_session: AsyncSession):
    repo = WalletRepository(db_session)
    wallet = await repo.create_wallet()

    balance = await repo.get_wallet_balance(wallet.id)

    assert_that(
        actual_or_assertion=balance,
        matcher=equal_to(Decimal(0)),
    )


@pytest.mark.asyncio
async def test_get_wallet_balance_not_found(db_session: AsyncSession):
    repo = WalletRepository(db_session)

    with pytest.raises(WalletNotFound):
        await repo.get_wallet_balance(uuid.uuid4())


@pytest.mark.asyncio
async def test_change_balance_deposit(db_session: AsyncSession):
    repo = WalletRepository(db_session)
    wallet = await repo.create_wallet()

    updated = await repo.change_balance(wallet.id, Decimal("150.50"))

    assert_that(
        actual_or_assertion=updated.id,
        matcher=equal_to(wallet.id),
    )
    assert_that(
        actual_or_assertion=updated.balance,
        matcher=equal_to(Decimal("150.50")),
    )

    balance = await repo.get_wallet_balance(wallet.id)
    assert_that(
        actual_or_assertion=balance,
        matcher=equal_to(Decimal("150.50")),
    )


@pytest.mark.asyncio
async def test_change_balance_withdraw(db_session: AsyncSession):
    repo = WalletRepository(db_session)
    wallet = await repo.create_wallet()
    await repo.change_balance(wallet.id, Decimal(200))

    updated = await repo.change_balance(wallet.id, Decimal(-50))

    assert_that(
        actual_or_assertion=updated.balance,
        matcher=equal_to(Decimal(150)),
    )


@pytest.mark.asyncio
async def test_change_balance_insufficient_funds(db_session: AsyncSession):
    repo = WalletRepository(db_session)
    wallet = await repo.create_wallet()
    await repo.change_balance(wallet.id, Decimal(30))

    with pytest.raises(InsufficientFundsError, match="Недостаточно средств"):
        await repo.change_balance(wallet.id, Decimal(-50))

    balance = await repo.get_wallet_balance(wallet.id)
    assert_that(
        actual_or_assertion=balance,
        matcher=equal_to(Decimal(30)),
    )
