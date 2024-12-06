from time import perf_counter

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


def part1() -> int:
    data: list[str] = [str.strip() for str in read_file(filename=INPUT_FILE)]
    safe_lines = 0
    for line in data:
        numbers = [int(num) for num in line.split()]
        is_safe_line, index = is_safe(numbers)
        if is_safe_line:
            safe_lines += 1
    return safe_lines


def part2() -> int:
    data: list[str] = [str.strip() for str in read_file(INPUT_FILE)]
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
