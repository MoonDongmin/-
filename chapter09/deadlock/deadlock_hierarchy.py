from lock_with_name import LockWithName

from deadlock import Philosopher

if __name__ == "__main__":
    chopstick_a = LockWithName("젓가락_a")
    chopstick_b = LockWithName("젓가락_b")

    philosopher_1 = Philosopher("철학자 #1", chopstick_a, chopstick_b)
    philosopher_2 = Philosopher("철학자 #2", chopstick_a, chopstick_b)

    philosopher_1.start()
    philosopher_2.start()
