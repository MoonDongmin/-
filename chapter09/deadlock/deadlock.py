import time
from threading import Thread

from lock_with_name import LockWithName

dumplings = 20


class Philosopher(Thread):
    def __init__(self, name: str, left_chopstick: LockWithName,
                 right_chopstick: LockWithName):
        super().__init__()
        self.name = name

        # 철학자와 철학자 사이에 젓가락 한 개씩 있음
        self.left_chopstick = left_chopstick
        self.right_chopstick = right_chopstick

    def run(self) -> None:
        global dumplings

        while dumplings > 0:  # 만두가 사라질 때까지 실행
            self.left_chopstick.acquire()  # 왼쪽에 있는 젓가락 집음
            print(f"{self.left_chopstick.name}을 {self.name}가 집는다"
                  f"이제 {self.right_chopstick.name}가 필요하다")
            self.right_chopstick.acquire()  # 오른쪽에 있는 젓가락 집음
            print(f"{self.right_chopstick.name}을 {self.name}가 집는다")
            dumplings -= 1  # 만두를 하나 먹음
            print(f"{self.name}가 만두를 먹는다. "
                  f"남은 만두의 수: {dumplings}")
            self.right_chopstick.release()  # 오른쪽 젓가락을 내려 놓음
            print(f"{self.right_chopstick.name}을 {self.name}가 내려놓는다")
            self.left_chopstick.release()  # 왼쪽 젓가락을 내려 놓음
            print(f"{self.left_chopstick.name}을 {self.name}가 내려놓는다")
            print(f"{self.name} 는 사색을 시작한다...")
            time.sleep(0.1)


if __name__ == "__main__":
    chopstick_a = LockWithName("젓가락_a")
    chopstick_b = LockWithName("젓가락_b")

    philosopher_1 = Philosopher("철학가 #1", chopstick_a, chopstick_b)
    philosopher_2 = Philosopher("철학가 #2", chopstick_b, chopstick_a)

    philosopher_1.start()
    philosopher_2.start()
