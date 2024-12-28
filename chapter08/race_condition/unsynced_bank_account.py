#!/usr/bin/env python3.9
"""Bank account without synchronization cause race condition """

from bank_account import BankAccount


class UnsyncedBankAccount(BankAccount):

    def deposit(self, amount: float) -> None:
        if amount > 0:
            self.balance += amount
        else:
            raise ValueError("0원 보다 작은 액수를 입금할 수 없습니다.")

    def withdraw(self, amount: float) -> None:
        if 0 < amount <= self.balance:
            self.balance -= amount
        else:
            raise ValueError("계좌에 잔고가 부족합니다.")
