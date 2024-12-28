from threading import Lock
from unsynced_bank_account import UnsyncedBankAccount


class SyncedBankAccount(UnsyncedBankAccount):

    def __init__(self, balance: float = 0):
        super().__init__(balance)
        self.mutex = Lock()

    def deposit(self, amount: float) -> None:
        # acquiring a lock on the shared resource
        self.mutex.acquire()
        super().deposit(amount)
        self.mutex.release()

    def withdraw(self, amount: float) -> None:
        self.mutex.acquire()
        super().withdraw(amount)
        self.mutex.release()
