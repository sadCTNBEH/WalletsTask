"""Модуль пользовательских исключений приложения."""


class WalletError(Exception):
    """Базовое исключение для ошибок кошелька."""

    def __init__(self, message: str = "Ошибка кошелька"):
        self.message = message
        super().__init__(self.message)


class WalletNotFound(WalletError):
    """Кошелёк не найден."""

    def __init__(self, message: str = "Кошелёк не найден"):
        super().__init__(message)


class InsufficientFundsError(WalletError):
    """Недостаточно средств."""

    def __init__(self, message: str = "Недостаточно средств"):
        super().__init__(message)
