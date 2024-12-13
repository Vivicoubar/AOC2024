from time import perf_counter
from collections import deque
from sys import stdout

EX_FILE: str = "./AOC10/ex1.txt"
INPUT_FILE: str = "./AOC10/input1.txt"

DISTINCT_POS: dict[tuple[int, int], int] = {}


def read_file(filename) -> str:
    with open(filename, "r") as file:
        return file.read().strip()


def count_distinct_trails(grid, start_row, start_col) -> int:
    # Recursive function to count the number of distinct trails
    if grid[start_row][start_col] == 9:  # We reach the beginning o
        return 1
    if (start_row, start_col) in DISTINCT_POS:
        return DISTINCT_POS[(start_row, start_col)]
    res = 0
    movements: list[tuple[int, int]] = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    for movement in movements:
        new_row = start_row + movement[0]
        new_col = start_col + movement[1]
        if (
            0 <= new_row < len(grid)
            and 0 <= new_col < len(grid[0])
            and grid[new_row][new_col] == grid[start_row][start_col] + 1
        ):
            res += count_distinct_trails(grid, new_row, new_col)
    DISTINCT_POS[(start_row, start_col)] = res
    return res


def count_trails_bfs(grid, start_row, start_col) -> int:
    movements: list[tuple[int, int]] = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    queue: deque = deque([(start_row, start_col)])
    seen: set = set()
    max_rows: int = len(grid)
    max_cols: int = len(grid[0])
    res = 0
    while queue:
        row, col = queue.popleft()
        if (row, col) in seen:
            continue
        seen.add((row, col))
        if grid[row][col] == 9:
            res += 1
        for movement in movements:
            new_row = row + movement[0]
            new_col = col + movement[1]
            if (
                0 <= new_row < max_rows
                and 0 <= new_col < max_cols
                and grid[new_row][new_col] == grid[row][col] + 1
            ):
                queue.append((new_row, new_col))
    return res


def part1(file) -> int:
    str_grid: list[str] = read_file(file).split("\n")
    grid: list[list[int]] = [[int(x) for x in row] for row in str_grid]
    p1: int = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 0:
                p1 += count_trails_bfs(grid, row, col)
    return p1


def part2(file) -> int:
    str_grid: list[str] = read_file(file).split("\n")
    grid: list[list[int]] = [[int(x) for x in row] for row in str_grid]
    p2: int = 0
    DISTINCT_POS.clear()
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 0:
                p2 += count_distinct_trails(grid, row, col)
    return p2


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
    benchmark_p1(20)
    benchmark_p2(20)


if __name__ == "__main__":
    show_results()
    write_output("./AOC10/output_code.txt")
