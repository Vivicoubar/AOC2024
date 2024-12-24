from time import perf_counter
from sys import stdout

EX_FILE = "./AOC19/ex1.txt"
INPUT_FILE = "./AOC19/input1.txt"


def read_file(file):
    with open(file) as f:
        return f.read().strip()


DYNAMIC_PROG_DICT = {}


def count_possibilities(words, target):
    if target in DYNAMIC_PROG_DICT:
        return DYNAMIC_PROG_DICT[target]
    ans = 0
    if not target:
        ans = 1
    for word in words:
        if target.startswith(word):
            ans += count_possibilities(words, target[len(word):])
    DYNAMIC_PROG_DICT[target] = ans
    return ans


def part1and2(file):
    DYNAMIC_PROG_DICT.clear()
    p1 = 0
    p2 = 0
    D = read_file(file)
    words, targets = D.split("\n\n")
    words = words.split(", ")
    for target in targets.split("\n"):
        target_ways = count_possibilities(words, target)
        if target_ways > 0:
            p1 += 1
        p2 += target_ways
    return p1, p2


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
    print(f"Part 1 & 2:{(secs) / n_iter:.7f} s")


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
    write_output("./AOC19/output_code.txt")
