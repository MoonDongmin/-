import time
from threading import Thread

from lock_with_name import LockWithName

dumplings = 20


class Philosopher(Thread):
    def __init__(self, name: str, left_chopstick: LockWithName,
                 right_chopstick: LockWithName):
        super().__init__()
        self.name = name
        self.left_chopstick = left_chopstick
        self.right_chopstick = right_chopstick

    def run(self) -> None:
        """Defines the behavior of the philosopher in the thread.
        Acquires the left and right chopsticks, then eats a dumpling.
        """
        # using globally shared variable
        global dumplings

        while dumplings > 0:
            self.left_chopstick.acquire()
            print(f"{self.left_chopstick.name}을 {self.name}가 집는다"
                  f"이제 {self.right_chopstick.name}가 필요하다")
            self.right_chopstick.acquire()
            print(f"{self.right_chopstick.name}을 {self.name}가 집는다")
            dumplings -= 1
            print(f"{self.name}가 만두를 먹는다. "
                  f"남은 만두의 수: {dumplings}")
            self.right_chopstick.release()
            print(f"{self.right_chopstick.name}을 {self.name}가 내려놓는다")
            self.left_chopstick.release()
            print(f"{self.left_chopstick.name}을 {self.name}가 내려놓는다")
            print(f"{self.name} 는 사색을 시작한다...")
            time.sleep(0.1)


if __name__ == "__main__":
    chopstick_a = LockWithName("chopstick_a")
    chopstick_b = LockWithName("chopstick_b")

    philosopher_1 = Philosopher("Philosopher #1", chopstick_a, chopstick_b)
    philosopher_2 = Philosopher("Philosopher #2", chopstick_b, chopstick_a)

    philosopher_1.start()
    philosopher_2.start()
