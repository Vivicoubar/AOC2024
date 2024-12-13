import re
from time import perf_counter
from sys import stdout

EX_FILE: str = "./AOC3/ex1.txt"
INPUT_FILE: str = "./AOC3/input1.txt"


def read_file(filename) -> str:
    with open(filename, "r") as file:
        return file.read().strip()


def get_match_regex(text) -> tuple[int, int]:
    res_1: int = 0
    res_2: int = 0
    is_enabled: bool = True
    for i in range(len(text)):
        if text[i:].startswith("do()"):
            is_enabled = True
        elif text[i:].startswith("don't()"):
            is_enabled = False
        matches: re.Match[str] | None = re.match(
            pattern=r"mul\((\d{1,3}),(\d{1,3})\)", string=text[i:]
        )
        if matches:
            res_1 += int(matches.group(1)) * int(matches.group(2))
            res_2 += int(matches.group(1)) * \
                int(matches.group(2)) if is_enabled else 0
    return res_1, res_2


def part1and2(file) -> tuple[int, int]:
    data: str = read_file(filename=file)
    return get_match_regex(data)


def benchmark_p1and2(n_iter: int) -> None:
    secs: float = 0
    print("Benchmark 1 and 2 -", n_iter, "iterations: ", end=" ")
    for _ in range(n_iter):
        start: float = perf_counter()
        part1and2(INPUT_FILE)
        end: float = perf_counter()
        secs += end - start
        print(".", end=" ")
        stdout.flush()
    print(f"Part 1 and 2: {(secs) / n_iter:.7f} s")


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
    write_output("./AOC3/output_code.txt")
