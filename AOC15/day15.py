from sys import stdout
from time import perf_counter
from collections import deque


INPUT_FILE = "./AOC15/input1.txt"
EX_FILE = "./AOC15/ex1.txt"

DIRS_DICT: dict[str, tuple[int, int]] = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1),
}


def build_double_grid(grid):
    double_grid = []
    for row in grid:
        double_row = []
        for cell in row:
            if cell == "#":
                double_row.append("#")
                double_row.append("#")
            elif cell == "O":
                double_row.append("[")
                double_row.append("]")
            elif cell == ".":
                double_row.append(".")
                double_row.append(".")
            elif cell == "@":
                double_row.append("@")
                double_row.append(".")
        double_grid.append(double_row)
    return double_grid


def read_file(file) -> str:
    with open(file) as f:
        return f.read().strip()


def calc_coords(grid):
    res = 0
    max_row = len(grid)
    max_col = len(grid[0])
    for row in range(max_row):
        for col in range(max_col):
            cell = grid[row][col]
            if cell == "[" or cell == "O":
                res += 100 * row + col
    return res


def part1and2(file: str, is_part2: bool = False) -> int:
    grid, commands = read_file(file).split("\n\n")
    grid = grid.split("\n")
    grid = [[grid[row][col]
             for col in range(len(grid[0]))] for row in range(len(grid))]
    max_row = len(grid)
    max_col = len(grid[0])
    if is_part2:
        grid = build_double_grid(grid)
        max_col *= 2
    start_row, start_col = 0, 0
    # Find the starting position
    for row in range(max_row):
        for col in range(max_col):
            if grid[row][col] == "@":
                start_row, start_col = row, col
                grid[row][col] = "."
    row, col = start_row, start_col
    for command in commands:
        # Execute the command
        if command == "\n":
            continue
        dir_row, dir_col = DIRS_DICT[command]
        new_row, new_col = row + dir_row, col + dir_col
        if grid[new_row][new_col] == "#":
            continue
        elif grid[new_row][new_col] == ".":
            row, col = new_row, new_col
        elif grid[new_row][new_col] in ["[", "]", "O"]:
            # If the cell is a crate, check if we can push it
            queue = deque([(row, col)])
            seen = set()
            is_correct = True
            while queue:
                # BFS to check how many crates we have to push and if we can
                # push them
                cur_row, cur_col = queue.popleft()
                if (cur_row, cur_col) in seen:
                    continue
                seen.add((cur_row, cur_col))
                next_cur_row, next_cur_col = cur_row + dir_row, cur_col + dir_col
                if grid[next_cur_row][next_cur_col] == "#":
                    is_correct = False
                    break
                elif grid[next_cur_row][next_cur_col] == "O":
                    queue.append((next_cur_row, next_cur_col))
                elif grid[next_cur_row][next_cur_col] == "[":
                    queue.append((next_cur_row, next_cur_col))
                    queue.append((next_cur_row, next_cur_col + 1))
                elif grid[next_cur_row][next_cur_col] == "]":
                    queue.append((next_cur_row, next_cur_col))
                    queue.append((next_cur_row, next_cur_col - 1))
            if not is_correct:
                continue
            # Push the crates
            while len(seen) > 0:
                for cur_row, cur_col in sorted(seen):
                    next_cur_row, next_cur_col = cur_row + dir_row, cur_col + dir_col
                    if (next_cur_row, next_cur_col) not in seen:
                        grid[next_cur_row][next_cur_col] = grid[cur_row][cur_col]
                        grid[cur_row][cur_col] = "."
                        seen.remove((cur_row, cur_col))
            row, col = row + dir_row, col + dir_col
    return calc_coords(grid)


def benchmark_p1(n_iter: int) -> None:
    secs: float = 0
    print("Benchmark 1 -", n_iter, "iterations: ", end=" ")
    for _ in range(n_iter):
        start: float = perf_counter()
        part1and2(INPUT_FILE)
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
        part1and2(INPUT_FILE, True)
        end: float = perf_counter()
        secs += end - start
        print(".", end=" ")
        stdout.flush()
    print(f"Part 2: {(secs) / n_iter:.7f} s")


def write_output(output_file):
    res_ex1 = part1and2(EX_FILE)
    res_ex2 = part1and2(EX_FILE, True)
    res_1 = part1and2(INPUT_FILE)
    res_2 = part1and2(INPUT_FILE, True)
    # Write the output in the format required (4 lines)
    with open(output_file, "w") as f:
        # Example Input results
        f.write(f"{res_ex1}\n")
        f.write(f"{res_ex2}\n")
        # Real Input results
        f.write(f"{res_1}\n")
        f.write(f"{res_2}\n")


def show_results():
    res_ex1 = part1and2(EX_FILE)
    res_ex2 = part1and2(EX_FILE, True)
    res_1 = part1and2(INPUT_FILE)
    res_2 = part1and2(INPUT_FILE, True)
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
    write_output("./AOC15/output_code.txt")
