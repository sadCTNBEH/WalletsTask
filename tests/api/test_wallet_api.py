"""Тесты слоя API"""

import uuid

import pytest
from hamcrest import assert_that, equal_to, has_entries, has_key
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_wallet_balance_success(client: AsyncClient):
    create = await client.post(url="api/v1/wallet")

    wallet_id = create.json()["id"]

    response = await client.get(f"/api/v1/wallet/{wallet_id}")
    assert_that(
        actual_or_assertion=response.status_code,
        matcher=equal_to(200),
    )
    assert_that(
        actual_or_assertion=response.json(),
        matcher=has_entries(
            id=equal_to(wallet_id),
            balance=equal_to("0.00"),
        ),
    )


@pytest.mark.asyncio
async def test_get_wallet_balance_not_found(client: AsyncClient):
    response = await client.get(f"/api/v1/wallet/{uuid.uuid4()}")

    assert_that(
        actual_or_assertion=response.status_code,
        matcher=equal_to(404),
    )
    assert_that(
        actual_or_assertion=response.json(),
        matcher=has_key("detail"),
    )


@pytest.mark.asyncio
async def test_deposit_success(client: AsyncClient):
    create = await client.post(url="api/v1/wallet")
    wallet_id = create.json()["id"]

    response = await client.post(
        url=f"/api/v1/wallet/{wallet_id}/operation",
        json={"operation_type": "DEPOSIT", "amount": "150"},
    )

    assert_that(
        actual_or_assertion=response.status_code,
        matcher=equal_to(200),
    )
    assert_that(
        actual_or_assertion=response.json(),
        matcher=has_entries(
            id=equal_to(wallet_id),
            balance=equal_to("150.00"),
        ),
    )


@pytest.mark.asyncio
async def test_deposit_invalid_amount_negative(client: AsyncClient):
    create = await client.post(url="api/v1/wallet")
    wallet_id = create.json()["id"]

    response = await client.post(
        url=f"/api/v1/wallet/{wallet_id}/operation",
        json={"operation_type": "DEPOSIT", "amount": "-150"},
    )

    assert_that(
        actual_or_assertion=response.status_code,
        matcher=equal_to(422),
    )


@pytest.mark.asyncio
async def test_withdraw_success(client: AsyncClient):
    create = await client.post(url="api/v1/wallet")
    wallet_id = create.json()["id"]

    await client.post(
        url=f"/api/v1/wallet/{wallet_id}/operation",
        json={"operation_type": "DEPOSIT", "amount": "150"},
    )

    response = await client.post(
        url=f"/api/v1/wallet/{wallet_id}/operation",
        json={"operation_type": "WITHDRAW", "amount": "100"},
    )

    assert_that(
        actual_or_assertion=response.status_code,
        matcher=equal_to(200),
    )
    assert_that(
        actual_or_assertion=response.json(),
        matcher=has_entries(
            id=equal_to(wallet_id),
            balance=equal_to("50.00"),
        ),
    )


@pytest.mark.asyncio
async def test_withdraw_insufficient_funds(client: AsyncClient):
    create = await client.post(url="api/v1/wallet")
    wallet_id = create.json()["id"]

    response = await client.post(
        url=f"/api/v1/wallet/{wallet_id}/operation",
        json={"operation_type": "WITHDRAW", "amount": "100"},
    )

    assert_that(
        actual_or_assertion=response.status_code,
        matcher=equal_to(400),
    )
    assert_that(
        actual_or_assertion=response.json(),
        matcher=has_key("detail"),
    )

@pytest.mark.asyncio
async def test_operation_invalid_amount_zero(client: AsyncClient):
    create = await client.post(url="api/v1/wallet")
    wallet_id = create.json()["id"]

    response = await client.post(
        url=f"/api/v1/wallet/{wallet_id}/operation",
        json={"operation_type": "DEPOSIT", "amount": "0"},
    )

    assert_that(
        actual_or_assertion=response.status_code,
        matcher=equal_to(422),
    )


@pytest.mark.asyncio
async def test_operation_invalid_type(client: AsyncClient):
    create = await client.post(url="api/v1/wallet")
    wallet_id = create.json()["id"]

    response = await client.post(
        url=f"/api/v1/wallet/{wallet_id}/operation",
        json={"operation_type": "TRANSFER", "amount": "10"},
    )

    assert_that(
        actual_or_assertion=response.status_code,
        matcher=equal_to(422),
    )
