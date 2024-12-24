from time import perf_counter
from sys import stdout
from collections import deque

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
EX_FILE: str = "./AOC18/ex1.txt"
INPUT_FILE: str = "./AOC18/input1.txt"


def read_file(file: str) -> str:
    with open(file, "r") as f:
        return f.read().strip()


def do_bfs(grid, grid_size) -> int | None:
    # BFS
    queue = deque([(0, 0, 0)])
    seen_pos = set()
    while queue:
        row, col, steps = queue.popleft()
        if (row, col) in seen_pos:
            continue
        seen_pos.add((row, col))
        if (row, col) == (grid_size - 1, grid_size - 1):
            return steps
        for dr, dc in DIRECTIONS:
            new_row, new_col = row + dr, col + dc
            if (
                0 <= new_row < grid_size
                and 0 <= new_col < grid_size
                and grid[new_row][new_col] == "."
            ):
                queue.append((new_row, new_col, steps + 1))
    return None


def part1(is_ex=False) -> int:
    if is_ex:
        file = EX_FILE
        grid_size = 7
        length = 12
    else:
        file = INPUT_FILE
        grid_size = 71
        length = 1024
    grid = [["." for _ in range(grid_size)] for _ in range(grid_size)]
    coors = [tuple(map(int, line.split(",")))
             for line in read_file(file).splitlines()]
    for i in range(length):
        row, col = coors[i]
        grid[col][row] = "#"
    res = do_bfs(grid, grid_size)
    return res if res else -1


def part2(is_ex=False) -> tuple[int, int]:
    if is_ex:
        file = EX_FILE
        grid_size = 7
        length = 12
    else:
        file = INPUT_FILE
        grid_size = 71
        length = 1024
    grid = [["." for _ in range(grid_size)] for _ in range(grid_size)]
    coors: list[tuple[int, int]] = []
    for line in read_file(file).splitlines():
        in_row, in_col = map(int, line.split(","))
        coors.append((in_row, in_col))
    for coord in coors:
        row, col = coord
        grid[col][row] = "#"
    for i in range(len(coors) - 1, length, -1):
        row, col = coors[i]
        grid[col][row] = "."
        res = do_bfs(grid, grid_size)
        if res:
            return coors[i]
    return -1, -1


def benchmark_p1(n_iter: int) -> None:
    secs: float = 0
    print("Benchmark 1 -", n_iter, "iterations: ", end=" ")
    for _ in range(n_iter):
        start: float = perf_counter()
        part1()
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
        part2()
        end: float = perf_counter()
        secs += end - start
        print(".", end=" ")
        stdout.flush()
    print(f"Part 2: {(secs) / n_iter:.7f} s")


def write_output(output_file):
    res_ex1, res_ex2 = part1(True), part2(True)
    res_1, res_2 = part1(), part2()
    # Write the output in the format required (4 lines)
    with open(output_file, "w") as f:
        # Example Input results
        f.write(f"{res_ex1}\n")
        f.write(f"{res_ex2}\n")
        # Real Input results
        f.write(f"{res_1}\n")
        f.write(f"{res_2}\n")


def show_results():
    res_ex1, res_ex2 = part1(True), part2(True)
    res_1, res_2 = part1(), part2()
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
    write_output("./AOC18/output_code.txt")
