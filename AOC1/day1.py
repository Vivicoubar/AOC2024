from numpy import ndarray, sort
from time import perf_counter
from sys import stdout

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


def part1(file: str) -> int:
    data: list[str] = [str.strip() for str in read_file(file)]
    list_a, list_b = get_sorted_arrays(data)
    res = 0
    for i in range(len(list_a)):
        res += abs(list_b[i] - list_a[i])
    return res


def part2(file: str) -> int:
    data: list[str] = [str.strip() for str in read_file(file)]
    list_a, list_b = get_data_arrays(data)
    res = 0
    for i in range(len(list_a)):
        res += list_a[i] * list_b.count(list_a[i])
    return res


def benchmark_p1(n_iter: int) -> None:
    secs: float = 0
    print("Benchmark 1 -", n_iter, "iterations: ", end=" ")
    for _ in range(n_iter):
        start: float = perf_counter()
        part1(INPUT_FILE)
        end: float = perf_counter()
        secs += end - start
        print(".", end=" ")
        stdout.flush()
    print(f"Part 1: {(secs) / n_iter:.7f} s")


def benchmark_p2(n_iter: int) -> None:
    secs: float = 0
    print("Benchmark 2 -", n_iter, "iterations: ", end=" ")
    for _ in range(n_iter):
        start: float = perf_counter()
        part2(INPUT_FILE)
        end: float = perf_counter()
        secs += end - start
        print(".", end=" ")
        stdout.flush()
    print(f"Part 2: {(secs) / n_iter:.7f} s")


def write_output(output_file):
    res_ex1 = part1(EX_FILE)
    res_ex2 = part2(EX_FILE)
    res_1 = part1(INPUT_FILE)
    res_2 = part2(INPUT_FILE)
    # Write the output in the format required (4 lines).
    with open(output_file, "w") as f:
        # Example Input results
        f.write(f"{res_ex1}\n")
        f.write(f"{res_ex2}\n")
        # Real Input results
        f.write(f"{res_1}\n")
        f.write(f"{res_2}\n")


def show_results():
    res_ex1 = part1(EX_FILE)
    res_ex2 = part2(EX_FILE)
    res_1 = part1(INPUT_FILE)
    res_2 = part2(INPUT_FILE)
    print("----- [Results] -----")
    print("Res EX 1: " + str(res_ex1))
    print("Res EX 2: " + str(res_ex2))
    print("Res 1: " + str(res_1))
    print("Res 2: " + str(res_2))
    print("--- [Benchmarks] ---")
    benchmark_p1(20)
    benchmark_p2(20)


if __name__ == "__main__":
    show_results()
    write_output("./AOC1/output_code.txt")
