import os
import math
import time
import typing as T
import hashlib
from multiprocessing import Pool

ChunkRange = T.Tuple[int, int]


def get_combinations(*, length: int, min_number: int = 0, max_number: int = None) -> T.List[str]:
    """Generate all possible password combinations"""
    combinations = []
    if not max_number:
        # calculating maximum number based on the length
        max_number = int(math.pow(10, length) - 1)

    # go through all possible combinations in a given range
    for i in range(min_number, max_number + 1):
        str_num = str(i)
        # fill in the missing numbers with zeros
        zeros = "0" * (length - len(str_num))
        combinations.append("".join((zeros, str_num)))
    return combinations


def get_crypto_hash(password: str) -> str:
    """"Calculating cryptographic hash of the password"""
    return hashlib.sha256(password.encode()).hexdigest()


def check_password(expected_crypto_hash: str,
                   possible_password: str) -> bool:
    actual_crypto_hash = get_crypto_hash(possible_password)
    # compare the resulted cryptographic hash with the one stored on the system
    return expected_crypto_hash == actual_crypto_hash


def get_chunks(num_ranges: int,
               length: int) -> T.Iterator[ChunkRange]:
    """Splitting the passwords into chunks using break points"""
    max_number = int(math.pow(10, length) - 1)
    chunk_starts = [int(max_number / num_ranges * i)
                    for i in range(num_ranges)]
    chunk_ends = [start_point - 1
                  for start_point in
                  chunk_starts[1:]] + [max_number]
    return zip(chunk_starts, chunk_ends)


def crack_chunk(crypto_hash: str, length: int, chunk_start: int,
                chunk_end: int) -> T.Union[str, None]:
    """Brute force the password combinations"""
    print(f"{chunk_start}부터 {chunk_end}까지 처리하는 중")
    combinations = get_combinations(length=length, min_number=chunk_start,
                                    max_number=chunk_end)
    for combination in combinations:
        if check_password(crypto_hash, combination):
            return combination  # found it
    return  # not found


def crack_password_parallel(crypto_hash: str, length: int) -> None:
    """Orchestrate cracking the password between different processes"""
    # getting number of available processors
    num_cores = os.cpu_count()
    print("패트워드 후보를 동시적으로 처리하는 중")
    start_time = time.perf_counter()

    # processing each chunk in a separate process concurrently
    with Pool() as pool:
        arguments = ((crypto_hash, length, chunk_start, chunk_end) for
                     chunk_start, chunk_end in
                     get_chunks(num_cores, length))
        results = pool.starmap(crack_chunk, arguments)
        print("후보 뭉치의 처리 원리를 기다리는 중")
        pool.close()
        pool.join()

    result = [res for res in results if res]
    print(f"크랙된 패스워드: {result[0]}")
    process_time = time.perf_counter() - start_time
    print(f"처리 시간: {process_time}")


if __name__ == "__main__":
    crypto_hash = \
        "e24df920078c3dd4e7e8d2442f00e5c9ab2a231bb3918d65cc50906e49ecaef4"
    length = 8
    crack_password_parallel(crypto_hash, length)
