"""Модуль с перечислениями, используемыми в приложении."""

from enum import Enum


class OperationType(str, Enum):
    """
    Типы операций изменения баланса кошелька.

    Attributes:
        DEPOSIT: Пополнение кошелька.
        WITHDRAW: Снятие средств с кошелька.
    """

    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"
