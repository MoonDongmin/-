from __future__ import annotations

import typing as T
from collections import deque
from random import randint

Result = T.Any
Burger = Result
Coroutine = T.Callable[[], 'Future']


class Future:

    def __init__(self) -> None:
        self.done = False
        self.coroutine = None
        self.result = None

    def set_coroutine(self, coroutine: Coroutine) -> None:
        self.coroutine = coroutine

    def set_result(self, result: Result) -> None:
        self.done = True
        self.result = result

    def __iter__(self) -> Future:
        return self

    def __next__(self) -> Result:
        if not self.done:
            raise StopIteration
        return self.result


class EventLoop:
    def __init__(self) -> None:
        self.tasks: T.Deque[Coroutine] = deque()

    def add_coroutine(self, coroutine: Coroutine) -> None:
        self.tasks.append(coroutine)

    def run_coroutine(self, task: T.Callable) -> None:
        future = task()
        future.set_coroutine(task)
        try:
            next(future)
            if not future.done:
                future.set_coroutine(task)
                self.add_coroutine(task)
        except StopIteration:
            return

    def run_forever(self) -> None:
        while self.tasks:
            self.run_coroutine(self.tasks.popleft())


def cook(on_done: T.Callable[[Burger], None]) -> None:
    burger: str = f"햄버거 #{randint(1, 10)}"
    print(f"{burger}의 조리가 끝났습니다!")
    on_done(burger)


def cashier(burger: Burger, on_done: T.Callable[[Burger], None]) -> None:
    print("주문하신 햄버거 포장이 완료되었습니다!")
    on_done(burger)


def order_burger() -> Future:
    order = Future()

    def on_cook_done(burger: Burger) -> None:
        cashier(burger, on_cashier_done)

    def on_cashier_done(burger: Burger) -> None:
        print(f"{burger}? 내 주문이에요!")
        order.set_result(burger)

    cook(on_cook_done)
    return order


if __name__ == "__main__":
    event_loop = EventLoop()
    event_loop.add_coroutine(order_burger)
    event_loop.run_forever()
