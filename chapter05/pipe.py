from threading import Thread, current_thread
from multiprocessing import Pipe
from multiprocessing.connection import Connection


class Writer(Thread):
    """Writer thread will write messages into the pipe"""

    def __init__(self, conn: Connection):
        super().__init__()
        self.conn = conn
        self.name = "Writer"

    def run(self) -> None:
        print(f"{current_thread().name}: 고무 오리를 보내는 중...\n")
        self.conn.send("Rubber duck")


class Reader(Thread):
    """Reader thread will read messages from the pipe"""

    def __init__(self, conn: Connection):
        super().__init__()
        self.conn = conn
        self.name = "Reader"

    def run(self) -> None:
        print(f"{current_thread().name}: 데이터를 읽는 중...")
        msg = self.conn.recv()
        print(f"{current_thread().name}: 전달받은 데이터: {msg}")


def main() -> None:
    # Connections for reading and writing
    reader_conn, writer_conn = Pipe()
    reader = Reader(reader_conn)
    writer = Writer(writer_conn)

    threads = [
        writer,
        reader
    ]
    # start threads
    for thread in threads:
        thread.start()

    # block the main thread until the child threads has finished
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
