import re
from typing import NamedTuple
from time import perf_counter
from sys import stdout


INPUT_FILE = "./AOC14/input1.txt"
EX_FILE = "./AOC14/ex1.txt"


class Robot(NamedTuple):
    px: int
    py: int
    vx: int
    vy: int


def read_input(file):
    with open(file) as f:
        return f.read().strip()


def get_robots(data: str) -> list[Robot]:
    robots = []
    for line in data.split("\n"):
        px, py, vx, vy = [int(x) for x in re.findall(r"-?\d+", line)]
        robots.append(Robot(px, py, vx, vy))
    return robots


def calc_security_score(robots: list[Robot], X: int, Y: int, t: int) -> int:
    q1, q2, q3, q4 = 0, 0, 0, 0
    for robot in robots:
        n_px = (robot.px + robot.vx * t) % X
        n_py = (robot.py + robot.vy * t) % Y
        if n_px < X // 2 and n_py < Y // 2:
            q1 += 1
        if n_px > X // 2 and n_py < Y // 2:
            q2 += 1
        if n_px < X // 2 and n_py > Y // 2:
            q3 += 1
        if n_px > X // 2 and n_py > Y // 2:
            q4 += 1
    return q1 * q2 * q3 * q4


def part1(file, is_example: bool = False) -> int:
    data: str = read_input(file)
    robots: list[Robot] = get_robots(data)
    X = 101 if not is_example else 11
    Y = 103 if not is_example else 7
    return calc_security_score(robots, X, Y, 100)


def part2(file, is_example: bool = False) -> int:
    data = read_input(file)
    robots = get_robots(data)
    X = 101 if not is_example else 11
    Y = 103 if not is_example else 7
    for t in range(10**6):
        SEEN = set()
        for robot in robots:
            n_px = (robot.px + robot.vx * t) % X
            n_py = (robot.py + robot.vy * t) % Y
            if (n_px, n_py) in SEEN:
                break
            else:
                SEEN.add((n_px, n_py))
        if len(SEEN) == len(robots):
            return t
    return -1


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
    res_ex1: int = part1(EX_FILE, True)
    res_ex2: int = part2(EX_FILE, True)
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
    res_ex1: int = part1(EX_FILE, True)
    res_ex2: int = part2(EX_FILE, True)
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
    show_results()
    write_output("./AOC14/output_code.txt")
