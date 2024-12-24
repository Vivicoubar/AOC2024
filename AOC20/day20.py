from heapq import heappush, heappop, heapify
import math
from time import perf_counter
from sys import stdout
from typing import NamedTuple

EX_FILE = "./AOC20/ex1.txt"
INPUT_FILE = "./AOC20/input1.txt"


class Pos(NamedTuple):
    x: int
    y: int


def read_input(file) -> list[list[str]]:
    with open(file, "r") as f:
        return [[c for c in line.strip()] for line in f.readlines()]


def get_cardinal_neighbors(grid, x, y):
    neighbors = []
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
            neighbors.append((nx, ny))
    return neighbors


def a_star_search(grid, start: Pos, end: Pos):
    def heuristic(next_point) -> int:
        return abs(next_point[0] - end[0]) + abs(next_point[1] - end[1])

    frontier: list[tuple[int, Pos]] = [(0, start)]
    heapify(frontier)
    came_from = {}
    cost_so_far = {start: 0}
    while frontier:
        current: Pos = heappop(frontier)[1]
        if current == end:
            break
        for next_point in get_cardinal_neighbors(grid, current[0], current[1]):
            if grid[next_point[1]][next_point[0]] == "#":
                continue
            new_cost = cost_so_far[current] + 1
            if next_point not in cost_so_far or new_cost < cost_so_far[next_point]:
                cost_so_far[next_point] = new_cost
                priority = new_cost + heuristic(next_point)
                heappush(frontier, (priority, next_point))
                came_from[next_point] = current
    return cost_so_far[end], came_from


def get_path(came_from, start, end):
    current = end
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path


def part1and2(file, is_part2=False):
    MAX_CHEAT_TIME = 2
    if is_part2:
        MAX_CHEAT_TIME = 20
    grid = read_input(file)
    start = Pos(-1, -1)
    end = Pos(-1, -1)
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == "S":
                start = Pos(x, y)
            elif cell == "E":
                end = Pos(x, y)

    assert start != Pos(-1, -1) and end != Pos(-1, -1)
    _, normal_came_from = a_star_search(grid, start, end)
    normal_path = get_path(normal_came_from, start, end)

    saved_time = 0
    for start_time, cheat in enumerate(normal_path):
        if start_time > len(normal_path) - 100:
            break
        i = start_time + 100
        while i < len(normal_path):
            cheat_end = normal_path[i]
            cheat_dist = abs(cheat_end[0] - cheat[0]) + \
                abs(cheat_end[1] - cheat[1])
            if cheat_dist > MAX_CHEAT_TIME:
                i += math.ceil(cheat_dist - MAX_CHEAT_TIME)
            else:
                cheat_end_time = start_time + cheat_dist
                saved = i - cheat_end_time
                if saved >= 100:
                    saved_time += 1
                i += 1
    return saved_time


def benchmark_p1(n_iter: int) -> None:
    secs: float = 0
    print("Benchmark 1 -", n_iter, "iterations: ", end=" ")
    for _ in range(n_iter):
        start: float = perf_counter()
        part1and2(INPUT_FILE, True)
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
        part1and2(INPUT_FILE, False)
        end: float = perf_counter()
        secs += end - start
        print(".", end=" ")
        stdout.flush()
    print(f"Part 2: {(secs) / n_iter:.7f} s")


def write_output(output_file):
    res_ex1, res_ex2 = part1and2(EX_FILE), part1and2(EX_FILE, True)
    res_1, res_2 = part1and2(INPUT_FILE), part1and2(INPUT_FILE, True)
    # Write the output in the format required (4 lines)
    with open(output_file, "w") as f:
        # Example Input results
        f.write(f"{res_ex1}\n")
        f.write(f"{res_ex2}\n")
        # Real Input results
        f.write(f"{res_1}\n")
        f.write(f"{res_2}\n")


def show_results():
    res_ex1, res_ex2 = part1and2(EX_FILE), part1and2(EX_FILE, True)
    res_1, res_2 = (
        part1and2(
            INPUT_FILE,
        ),
        part1and2(INPUT_FILE, True),
    )
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
    write_output("./AOC20/output_code.txt")
