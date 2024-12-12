from time import perf_counter
from sys import stdout

EX_FILE: str = "./AOC11/ex1.txt"
INPUT_FILE: str = "./AOC11/input1.txt"

DISTINCT_STONES: dict[tuple[int, int], int] = {}


def read_file(filename) -> str:
    with open(filename, "r") as file:
        return file.read().strip()


def blink_for_stone(stone, time) -> int:
    if (stone, time) in DISTINCT_STONES:
        return DISTINCT_STONES[(stone, time)]
    if time == 0:
        ans: int = 1
    elif stone == 0:
        ans: int = blink_for_stone(1, time - 1)
    elif len(str(stone)) % 2 == 0:
        half = len(str(stone)) // 2
        left = int(str(stone)[:half])
        right = int(str(stone)[half:])
        ans: int = blink_for_stone(left, time - 1) + \
            blink_for_stone(right, time - 1)
    else:
        ans: int = blink_for_stone(stone * 2024, time - 1)
    DISTINCT_STONES[(stone, time)] = ans
    return ans


def part1(file: str) -> int:
    DISTINCT_STONES.clear()
    stones: list[int] = [int(x) for x in read_file(file).split()]
    return sum(blink_for_stone(stone, 25) for stone in stones)


def part2(file: str) -> int:
    DISTINCT_STONES.clear()
    stones: list[int] = [int(x) for x in read_file(file).split()]
    return sum(blink_for_stone(stone, 75) for stone in stones)


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
    print(f"Part 1 :{(secs) / n_iter:.7f} s")


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
    res_ex1: int = part1(EX_FILE)
    res_ex2: int = part2(EX_FILE)
    res_1: int = part1(INPUT_FILE)
    res_2: int = part2(INPUT_FILE)
    # Write the output in the format required (4 lines)
    with open(output_file, "w") as f:
        # Example Input results
        f.write(f"{res_ex1}\n")
        f.write(f"{res_ex2}\n")
        # Real Input results
        f.write(f"{res_1}\n")
        f.write(f"{res_2}\n")


def show_results():
    res_ex1: int = part1(EX_FILE)
    res_ex2: int = part2(EX_FILE)
    res_1: int = part1(INPUT_FILE)
    res_2: int = part2(INPUT_FILE)
    print("----- [Results] -----")
    print("Res EX 1: " + str(res_ex1))
    print("Res EX 2: " + str(res_ex2))
    print("Res 1: " + str(res_1))
    print("Res 2: " + str(res_2))
    print("--- [Benchmarks] ---")
    benchmark_p1(20)
    benchmark_p2(20)


if __name__ == "__main__":
    # show_results()
    write_output("./AOC11/output_code.txt")
