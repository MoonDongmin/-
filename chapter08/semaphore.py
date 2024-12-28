import typing as T
import time
import random
from threading import Thread, Semaphore, Lock

TOTAL_SPOTS = 3


class Garage:

    def __init__(self) -> None:
        self.semaphore = Semaphore(TOTAL_SPOTS)
        self.cars_lock = Lock()
        self.parked_cars: T.List[str] = []

    def count_parked_cars(self) -> int:
        return len(self.parked_cars)

    def enter(self, car_name: str) -> None:
        """Enter the garage"""
        self.semaphore.acquire()
        self.cars_lock.acquire()
        self.parked_cars.append(car_name)
        print(f"{car_name} 주차 됨")
        self.cars_lock.release()

    def exit(self, car_name: str) -> None:
        """Car exits the garage"""
        self.cars_lock.acquire()
        self.parked_cars.remove(car_name)
        print(f"{car_name} 출차됨 ")
        self.semaphore.release()
        self.cars_lock.release()


def park_car(garage: Garage, car_name: str) -> None:
    """Emulate parked car behavior"""
    garage.enter(car_name)
    time.sleep(random.uniform(1, 2))
    garage.exit(car_name)


def test_garage(garage: Garage, number_of_cars: int = 10) -> None:
    threads = []
    for car_num in range(number_of_cars):
        t = Thread(target=park_car,
                   args=(garage, f"차량 #{car_num}"))
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    number_of_cars = 10
    garage = Garage()
    # test garage by concurrently arriving cars
    test_garage(garage, number_of_cars)

    print("주차장에 남아있는 차량 수: ")
    print(f"실제 수: {garage.count_parked_cars()}\n정상 수: 0")