from collections import defaultdict
from sys import stdout
from time import perf_counter


MODULO = 16777216
WINDOW_SIZE = 20**4
STEP_COUNT = 1997

EX_FILE, INPUT_FILE = "./AOC22/ex1.txt", "./AOC22/input1.txt"


def get_next_step(x):
    """Calculates the next value in the sequence"""
    x = ((x * 64) ^ x) % MODULO
    x = ((x // 32) ^ x) % MODULO
    x = ((x * 2048) ^ x) % MODULO
    return x


def read_file(file_path):
    with open(file_path, "r") as f:
        return [int(line) for line in f.read().strip().splitlines()]


def part1and2(file):
    p1 = 0
    bananas = defaultdict(int)
    data: list[int] = read_file(file)

    for step in data:
        window = 0
        for _ in range(4):
            next_step = get_next_step(step)
            window = (window * 20 + (next_step %
                      10) - (step % 10)) % WINDOW_SIZE
            step = next_step

        seen = set()
        for i in range(STEP_COUNT):
            if i == STEP_COUNT - 1:
                p1 += step

            if window not in seen:
                bananas[window] += step % 10
                seen.add(window)

            next_step = get_next_step(step)
            window = (window * 20 + (next_step %
                      10) - (step % 10)) % WINDOW_SIZE
            step = next_step

    return p1, max(bananas.values())


def benchmark_p1and2(n_iter: int) -> None:
    secs: float = 0
    print("Benchmark 1 & 2 -", n_iter, "iterations: ", end=" ")
    for _ in range(n_iter):
        start: float = perf_counter()
        part1and2(INPUT_FILE)
        end: float = perf_counter()
        secs += end - start
        print(".", end=" ")
        stdout.flush()
    print(f"Part 1 & 2 :{(secs) / n_iter:.7f} s")


def write_output(output_file):
    res_ex1, res_ex2 = part1and2(EX_FILE)
    res_1, res_2 = part1and2(INPUT_FILE)
    # Write the output in the format required (4 lines)
    with open(output_file, "w") as f:
        # Example Input results
        f.write(f"{res_ex1}\n")
        f.write(f"{res_ex2}\n")
        # Real Input results
        f.write(f"{res_1}\n")
        f.write(f"{res_2}\n")


def show_results():
    res_ex1, res_ex2 = part1and2(EX_FILE)
    res_1, res_2 = part1and2(INPUT_FILE)
    print("----- [Results] -----")
    print("Res EX 1: " + str(res_ex1))
    print("Res EX 2: " + str(res_ex2))
    print("Res 1: " + str(res_1))
    print("Res 2: " + str(res_2))
    print("--- [Benchmarks] ---")
    benchmark_p1and2(20)


if __name__ == "__main__":
    show_results()
    write_output("./AOC22/output_code.txt")
