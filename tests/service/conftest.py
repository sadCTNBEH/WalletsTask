"""Фикстуры для тестов слоя сервисов."""
from unittest.mock import AsyncMock

import pytest

from app.service.wallet import WalletService

@pytest.fixture
def mock_session():
    return AsyncMock()

@pytest.fixture
def mock_repository():
    return AsyncMock()

@pytest.fixture
def wallet_service(mock_session, mock_repository):
    service = WalletService(mock_session)
    service._repository = mock_repository

    return service