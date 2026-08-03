"""Тест сервиса кошельков."""

import uuid
from decimal import Decimal
from unittest.mock import MagicMock, AsyncMock

import pytest
from hamcrest import assert_that, instance_of, equal_to

from app.enums.wallet import OperationType
from app.exceptions.wallet import WalletNotFound, InsufficientFundsError
from app.models.wallet import Wallet
from app.schemas.wallet import WalletResponseModel


@pytest.mark.asyncio
async def test_get_wallet_balance_success(wallet_service, mock_repository):
    wallet_id = uuid.uuid4()
    mock_repository.get_wallet_balance.return_value = Decimal('100.50')

    result = await wallet_service.get_wallet_balance(wallet_id)

    assert_that(
        actual_or_assertion=result,
        matcher=instance_of(WalletResponseModel)
    )
    assert_that(
        actual_or_assertion=result.id,
        matcher=equal_to(wallet_id)
    )
    assert_that(
        actual_or_assertion=result.balance,
        matcher=equal_to(Decimal('100.50'))
    )
    mock_repository.get_wallet_balance.assert_awaited_once_with(wallet_id)

@pytest.mark.asyncio
async def test_get_wallet_balance_not_found(wallet_service, mock_repository, mock_session):
    wallet_id = uuid.uuid4()
    mock_repository.get_wallet_balance.side_effect = WalletNotFound()

    with pytest.raises(WalletNotFound):
        await wallet_service.get_wallet_balance(wallet_uuid=wallet_id)

    mock_repository.get_wallet_balance.assert_awaited_once_with(wallet_id)

@pytest.mark.asyncio
async def test_operation_deposit(wallet_service, mock_repository, mock_session, mocker):
    wallet_id = uuid.uuid4()
    wallet = MagicMock(spec=Wallet)
    wallet.balance = Decimal('150.50')
    mock_repository.change_balance.return_value = wallet

    mock_commit = mocker.patch(
        'app.service.wallet.commit_transaction',
        new_callable=AsyncMock,
    )

    result = await wallet_service.operation_wallet(
        wallet_uuid=wallet_id,
        operation_type=OperationType.DEPOSIT,
        amount=Decimal('150.50'),
    )

    assert_that(
        actual_or_assertion=result,
        matcher=instance_of(WalletResponseModel),
    )
    assert_that(
        actual_or_assertion=result.id,
        matcher=equal_to(wallet_id),
    )
    assert_that(
        actual_or_assertion=result.balance,
        matcher=equal_to(Decimal('150.50')),
    )
    mock_repository.change_balance.assert_awaited_once_with(
        wallet_id,
        Decimal('150.50'),
    )
    mock_commit.assert_awaited_once_with(mock_session)

@pytest.mark.asyncio
async def test_operation_withdraw(wallet_service, mock_repository, mock_session, mocker):
    wallet_id = uuid.uuid4()
    wallet = MagicMock(spec=Wallet)
    wallet.balance = Decimal('100')
    mock_repository.change_balance.return_value = wallet

    mock_commit = mocker.patch(
        'app.service.wallet.commit_transaction',
        new_callable=AsyncMock,
    )

    result = await wallet_service.operation_wallet(
        wallet_uuid=wallet_id,
        operation_type=OperationType.WITHDRAW,
        amount=Decimal('100'),
    )

    assert_that(
        actual_or_assertion=result.balance,
        matcher=equal_to(Decimal('100')),
    )
    mock_repository.change_balance.assert_awaited_once_with(
        wallet_id,
        Decimal('-100'),
    )
    mock_commit.assert_awaited_once_with(mock_session)

@pytest.mark.asyncio
async def test_operation_insufficient_funds(wallet_service, mock_repository, mocker):
    wallet_id = uuid.uuid4()
    mock_repository.change_balance.side_effect = InsufficientFundsError()

    mocker.patch(
        'app.service.wallet.commit_transaction',
        new_callable=AsyncMock,
    )

    with pytest.raises(InsufficientFundsError):
        await wallet_service.operation_wallet(
            wallet_uuid=wallet_id,
            operation_type=OperationType.WITHDRAW,
            amount=Decimal('100'),
        )

    mock_repository.change_balance.assert_awaited_once_with(
        wallet_id,
        Decimal('-100'),
    )

@pytest.mark.asyncio
async def test_operation_wallet_not_found(wallet_service, mock_repository, mocker):
    wallet_id = uuid.uuid4()
    mock_repository.change_balance.side_effect = WalletNotFound()

    mocker.patch(
        'app.service.wallet.commit_transaction',
        new_callable=AsyncMock,
    )

    with pytest.raises(WalletNotFound):
        await wallet_service.operation_wallet(
            wallet_uuid=wallet_id,
            operation_type=OperationType.WITHDRAW,
            amount=Decimal('100'),
        )

@pytest.mark.asyncio
async def test_operation_amount_zero(wallet_service, mock_repository):
    wallet_id = uuid.uuid4()

    with pytest.raises(ValueError, match='положительной'):
        await wallet_service.operation_wallet(
            wallet_uuid=wallet_id,
            operation_type=OperationType.DEPOSIT,
            amount=Decimal('0'),
        )

    mock_repository.change_balance.assert_not_awaited()

@pytest.mark.asyncio
async def test_operation_amount_negative(wallet_service, mock_repository):
    wallet_id = uuid.uuid4()

    with pytest.raises(ValueError, match='положительной'):
        await wallet_service.operation_wallet(
            wallet_uuid=wallet_id,
            operation_type=OperationType.DEPOSIT,
            amount=Decimal('-10'),
        )

    mock_repository.change_balance.assert_not_awaited()