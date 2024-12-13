import os
import time
import threading
from threading import Thread


def cpu_waster(i: int) -> None:
    name = threading.current_thread().getName()
    print(f"{name}가 작업 {i}를 수행 중")
    time.sleep(3)


def display_threads() -> None:
    print("-" * 10)
    print(f"현재 프로세스의 PID: {os.getpid()}")
    print(f"스레드 수: {threading.active_count()}")
    print("활성 스레드: ")
    for thread in threading.enumerate():
        print(thread)


def main(num_threads: int) -> None:
    display_threads()

    print(f"{num_threads}개의 CPU 낭비 프로그램 시작...")
    for i in range(num_threads):
        thread = Thread(target=cpu_waster, args=(i,))
        thread.start()

    display_threads()


if __name__ == "__main__":
    num_threads = 5
    main(num_threads)