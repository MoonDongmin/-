import time
from threading import Thread

from deadlock.lock_with_name import LockWithName

dumplings = 20


class Philosopher(Thread):
    def __init__(self, name: str, left_chopstick: LockWithName,
                 right_chopstick: LockWithName):
        super().__init__()
        self.name = name
        self.left_chopstick = left_chopstick
        self.right_chopstick = right_chopstick

    def run(self) -> None:
        # using globally shared variable
        global dumplings

        while dumplings > 0:
            self.left_chopstick.acquire()
            print(f"{self.left_chopstick.name}을  "
                  f"{self.name}가 집는다")
            if self.right_chopstick.locked():
                print(f"{self.name}는 "
                      f"{self.right_chopstick.name}을 잡지 못해, "
                      f"가지고 있던 젓가락을 내려 놓는다...")
            else:
                self.right_chopstick.acquire()
                print(f"{self.right_chopstick.name}을 "
                      f"{self.name}가 집는다")
                dumplings -= 1
                print(f"{self.name}는 만두를 먹는다. 남은 만두의 "
                      f"수: {dumplings}")
                print(f"{self.name}는 생각한다...")
                time.sleep(1)
                self.right_chopstick.release()
            self.left_chopstick.release()


if __name__ == "__main__":
    chopstick_a = LockWithName("젓가락_a")
    chopstick_b = LockWithName("젓가락_b")

    philosopher_1 = Philosopher("철학자 #1", chopstick_a, chopstick_b)
    philosopher_2 = Philosopher("철학자 #2", chopstick_b, chopstick_a)

    philosopher_1.start()
    philosopher_2.start()