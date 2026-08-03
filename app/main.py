"""Главный модуль приложения FastAPI."""

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.exceptions.handlers import insufficient_funds_handler, wallet_not_found_handler
from app.exceptions.wallet import InsufficientFundsError, WalletNotFound

app = FastAPI(
    title="Wallet API",
    description="API для управления кошельками и операциями с балансом.",
    version="1.0.0",
)

app.include_router(
    api_router,
    prefix="/api/v1",
)

app.add_exception_handler(WalletNotFound, wallet_not_found_handler)  # type: ignore[misc]
app.add_exception_handler(InsufficientFundsError, insufficient_funds_handler)  # type: ignore[misc]
