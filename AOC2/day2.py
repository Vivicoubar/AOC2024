from time import perf_counter
from sys import stdout

EX_FILE: str = "./AOC2/ex1.txt"
INPUT_FILE: str = "./AOC2/input1.txt"


def read_file(filename) -> list[str]:
    with open(filename, "r") as file:
        return file.readlines()


def is_safe(numbers: list[int]) -> tuple[bool, int]:
    state = ""
    if numbers[0] <= numbers[-1]:
        state = "increasing"
    else:
        state = "decreasing"
    for i in range(1, len(numbers)):
        if numbers[i] - numbers[i - 1] == 0:
            return False, i
        if state == "increasing":
            if numbers[i] - numbers[i - 1] > 3 or numbers[i] - \
                    numbers[i - 1] < 0:
                return False, i
        else:
            if numbers[i] - numbers[i - 1] < - \
                    3 or numbers[i] - numbers[i - 1] > 0:
                return False, i
    return True, 0


def part1(file) -> int:
    data: list[str] = [str.strip() for str in read_file(filename=file)]
    safe_lines = 0
    for line in data:
        numbers = [int(num) for num in line.split()]
        is_safe_line, index = is_safe(numbers)
        if is_safe_line:
            safe_lines += 1
    return safe_lines


def part2(file) -> int:
    data: list[str] = [str.strip() for str in read_file(file)]
    safe_lines = 0
    for line in data:
        numbers = [int(num) for num in line.split()]
        is_safe_line, index = is_safe(numbers)
        if is_safe_line:
            safe_lines += 1
        else:
            is_safe_line = False
            for i in range(len(numbers)):
                fixed_line = numbers[:i] + numbers[i + 1:]
                is_safe_line, index = is_safe(fixed_line)
                if is_safe_line:
                    safe_lines += 1
                    break
    return safe_lines


def benchmark_p1(n_iter: int) -> None:
    secs: float = 0
    print("Benchmark 1 -", n_iter, "iterations: ", end=" ")
    for _ in range(n_iter):
        start: float = perf_counter()
        part1(file=INPUT_FILE)
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
        part2(file=INPUT_FILE)
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
    # Write the output in the format required (4 lines)
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
    benchmark_p1(100)
    benchmark_p2(100)


if __name__ == "__main__":
    show_results()
    write_output("./AOC2/output_code.txt")
