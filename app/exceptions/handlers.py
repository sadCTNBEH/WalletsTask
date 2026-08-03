from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.exceptions.wallet import InsufficientFundsError, WalletNotFound


async def wallet_not_found_handler(
    request: Request, exc: WalletNotFound
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message},
    )


async def insufficient_funds_handler(
    request: Request, exc: InsufficientFundsError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message},
    )
