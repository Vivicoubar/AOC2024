from numpy import ndarray, sort
from time import perf_counter

EX_FILE: str = "./AOC1/ex1.txt"
INPUT_FILE: str = "./AOC1/input1.txt"


def read_file(filename) -> list[str]:
    with open(filename, "r") as file:
        return file.readlines()


def get_data_arrays(data: list[str]) -> tuple[list[int], list[int]]:
    list_a: list[int] = []
    list_b: list[int] = []
    for line in data:
        line_a_element, line_b_element = (
            int(line.split("   ")[0]),
            int(line.split("   ")[1]),
        )
        list_a.append(line_a_element)
        list_b.append(line_b_element)
    return list_a, list_b


def get_sorted_arrays(data: list[str]) -> tuple[ndarray, ndarray]:
    list_a: list[int] = []
    list_b: list[int] = []
    for line in data:
        line_a_element, line_b_element = (
            int(line.split("   ")[0]),
            int(line.split("   ")[1]),
        )
        list_a.append(line_a_element)
        list_b.append(line_b_element)
    return sort(list_a), sort(list_b)


def part1() -> int:
    data: list[str] = [str.strip() for str in read_file(EX_FILE)]
    list_a, list_b = get_sorted_arrays(data)
    res = 0
    for i in range(len(list_a)):
        res += abs(list_b[i] - list_a[i])
    return res


def part2() -> int:
    data: list[str] = [str.strip() for str in read_file(EX_FILE)]
    list_a, list_b = get_data_arrays(data)
    res = 0
    for i in range(len(list_a)):
        res += list_a[i] * list_b.count(list_a[i])
    return res


def benchmark_p1(n_iter: int) -> None:
    secs: float = 0
    for _ in range(n_iter):
        start: float = perf_counter()
        part1()
        end: float = perf_counter()
        secs += end - start
    print(f"Part 1: {(secs) / n_iter:.7f} s")


def benchmark_p2(n_iter: int) -> None:
    secs: float = 0
    for _ in range(n_iter):
        start: float = perf_counter()
        part2()
        end: float = perf_counter()
        secs += end - start
    print(f"Part 2: {(secs) / n_iter:.7f} s")


res_1 = part1()
res_2 = part2()
print("----- [Results] -----")
print("Res 1: " + str(res_1))
print("Res 2: " + str(res_2))
print("--- [Benchmarks] ---")
benchmark_p1(100)
benchmark_p2(100)
