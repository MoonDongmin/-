import time
from threading import Thread, Semaphore, Lock

SIZE = 5
# shared memory
BUFFER = ["" for i in range(SIZE)]
producer_idx: int = 0

mutex = Lock()
empty = Semaphore(SIZE)
full = Semaphore(0)


class Producer(Thread):
    def __init__(self, name: str, maximum_items: int = 5):
        super().__init__()
        self.counter = 0
        self.name = name
        self.maximum_items = maximum_items

    def next_index(self, index: int) -> int:
        return (index + 1) % SIZE

    def run(self) -> None:
        global producer_idx
        while self.counter < self.maximum_items:
            empty.acquire()
            mutex.acquire()
            self.counter += 1
            BUFFER[producer_idx] = f"{self.name}-{self.counter}"
            print(f"{self.name}가 물건을 생성함: "
                  f"'{BUFFER[producer_idx]}'를 슬롯 {producer_idx}에 넣음")
            producer_idx = self.next_index(producer_idx)
            mutex.release()
            full.release()
            time.sleep(1)


class Consumer(Thread):
    def __init__(self, name: str, maximum_items: int = 10):
        super().__init__()
        self.name = name
        self.idx = 0
        self.counter = 0
        self.maximum_items = maximum_items

    def next_index(self) -> int:
        return (self.idx + 1) % SIZE

    def run(self) -> None:
        while self.counter < self.maximum_items:
            full.acquire()
            mutex.acquire()
            item = BUFFER[self.idx]
            print(f"{self.name}가 물건을 처리함: "
                  f"'{item}'를 슬롯 {self.idx}에서 꺼냄")
            self.idx = self.next_index()
            self.counter += 1
            mutex.release()
            empty.release()
            time.sleep(2)


if __name__ == "__main__":
    threads = [
        Producer("스폰지밥"),
        Producer("뚱이"),
        Consumer("징징이")
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
