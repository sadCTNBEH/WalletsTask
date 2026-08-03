"""Модуль сборки API-маршрутов версии v1."""

from fastapi import APIRouter

from app.api.v1.wallet import router as wallet_router

api_router = APIRouter()

api_router.include_router(
    wallet_router,
)
