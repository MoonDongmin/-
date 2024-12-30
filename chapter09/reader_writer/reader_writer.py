import time
import random
from threading import Thread

from rwlock import RWLock

counter = 0
lock = RWLock()


class User(Thread):

    def __init__(self, idx: int):
        super().__init__()
        self.idx = idx

    def run(self) -> None:
        while True:
            lock.acquire_read()

            print(f"사용자 {self.idx}가 데이터를 읽는 중: {counter}")
            time.sleep(random.randrange(1, 3))

            lock.release_read()
            time.sleep(0.5)


class Librarian(Thread):

    def run(self) -> None:
        global counter
        while True:
            lock.acquire_write()

            print("사서가 데이터를 변경하는 중...")
            counter += 1
            print(f"새로운 값: {counter}")
            time.sleep(random.randrange(1, 3))

            lock.release_write()


if __name__ == "__main__":
    threads = [
        User(0),
        User(1),
        Librarian()
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
