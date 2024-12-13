from time import perf_counter
from sys import stdout
from typing import NamedTuple
import re

EX_FILE = "./AOC13/ex1.txt"
INPUT_FILE = "./AOC13/input1.txt"


class Machine(NamedTuple):
    # |a1 b1|   |x1|   |c1|
    # |a2 b2| X |x2| = |c2|
    a1: int
    a2: int
    b1: int
    b2: int
    c1: int
    c2: int


def read_file(filename: str) -> str:
    with open(filename, "r") as file:
        return file.read().strip()


def parse_machine(data: str) -> list[Machine]:
    machines: list[Machine] = []
    pattern = r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)"
    matches = re.findall(pattern, data)
    for match in matches:
        machine = Machine(
            int(match[0]),
            int(match[1]),
            int(match[2]),
            int(match[3]),
            int(match[4]),
            int(match[5]),
        )
        machines.append(machine)
    return machines


def solve_machine(machines: list[Machine], part2: bool = False) -> int:
    res = 0
    for machine in machines:
        part2_factor = 0
        if part2:
            part2_factor = 10000000000000
        deta = machine.a1 * machine.b2 - machine.a2 * machine.b1
        deta1 = (machine.c1 + part2_factor) * machine.b2 - (
            machine.c2 + part2_factor
        ) * machine.b1
        deta2 = machine.a1 * (part2_factor + machine.c2) - machine.a2 * (
            machine.c1 + part2_factor
        )
        if deta == 0 and (deta1 != 0 or deta2 != 0):
            continue
        x = deta1 / deta
        y = deta2 / deta
        # Check if x and y are integers
        if x != int(x) or y != int(y):
            continue
        res += int(x * 3 + y)
    return res


def part1(file: str) -> int:
    machines = parse_machine(read_file(file))
    return solve_machine(machines)


def part2(file: str) -> int:
    machines = parse_machine(read_file(file))
    return solve_machine(machines, True)


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
    write_output("./AOC13/output_code.txt")
