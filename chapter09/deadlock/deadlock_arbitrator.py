import time
from threading import Thread, Lock

from lock_with_name import LockWithName

dumplings = 20


class Waiter:
    def __init__(self) -> None:
        self.mutex = Lock()

    def ask_for_chopsticks(self, left_chopstick: LockWithName,
                           right_chopstick: LockWithName) -> None:
        with self.mutex:
            left_chopstick.acquire()
            print(f"{left_chopstick.name}을 집었다.")
            right_chopstick.acquire()
            print(f"{right_chopstick.name}을 집었다.")

    def release_chopsticks(self, left_chopstick: LockWithName,
                           right_chopstick: LockWithName) -> None:
        right_chopstick.release()
        print(f"{right_chopstick.name}을 내려 놓았다.")
        left_chopstick.release()
        print(f"{left_chopstick.name}을 내려 놓았다.\n")


class Philosopher(Thread):
    def __init__(self, name: str, waiter: Waiter,
                 left_chopstick: LockWithName,
                 right_chopstick: LockWithName):
        super().__init__()
        self.name = name
        self.left_chopstick = left_chopstick
        self.right_chopstick = right_chopstick
        self.waiter = waiter

    def run(self) -> None:
        # using globally shared variable
        global dumplings

        while dumplings > 0:
            print(f"{self.name} asks waiter for chopsticks")
            self.waiter.ask_for_chopsticks(
                self.left_chopstick, self.right_chopstick)

            dumplings -= 1
            print(f"{self.name} eats a dumpling. "
                  f"Dumplings left: {dumplings}")
            print(f"{self.name} returns chopsticks to waiter")
            self.waiter.release_chopsticks(
                self.left_chopstick, self.right_chopstick)
            time.sleep(0.1)


if __name__ == "__main__":
    chopstick_a = LockWithName("젓가락_a")
    chopstick_b = LockWithName("젓가락_b")

    waiter = Waiter()
    philosopher_1 = Philosopher("철학자 #1", waiter, chopstick_a,
                                chopstick_b)
    philosopher_2 = Philosopher("철학자 #2", waiter, chopstick_b,
                                chopstick_a)

    philosopher_1.start()
    philosopher_2.start()
