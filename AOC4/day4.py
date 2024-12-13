from time import perf_counter
from sys import stdout

EX_FILE: str = "./AOC4/ex1.txt"
INPUT_FILE: str = "./AOC4/input1.txt"


def read_file(filename) -> str:
    with open(filename, "r") as file:
        return file.read().strip()


word_patterns: list[list[list[int]]] = [
    [
        [0, 0],
        [0, 1],
        [0, 2],
        [0, 3],
    ],  # horizontal
    [
        [0, 3],
        [0, 2],
        [0, 1],
        [0, 0],
    ],  # reversed horizontal
    [
        [0, 0],
        [1, 0],
        [2, 0],
        [3, 0],
    ],  # vertical
    [
        [3, 0],
        [2, 0],
        [1, 0],
        [0, 0],
    ],  # reversed vertical
    [
        [0, 0],
        [1, 1],
        [2, 2],
        [3, 3],
    ],  # diagonal 1
    [
        [3, 3],
        [2, 2],
        [1, 1],
        [0, 0],
    ],  # reversed diagonal 1
    [
        [0, 3],
        [1, 2],
        [2, 1],
        [3, 0],
    ],  # diagonal 2
    [
        [3, 0],
        [2, 1],
        [1, 2],
        [0, 3],
    ],  # reversed diagonal 2
]

cross_patterns: list[list[list[int]]] = [
    [[0, 0], [1, 1], [2, 2], [2, 0], [1, 1], [0, 2]],
    # M.S
    # .A.
    # M.S
    [[0, 0], [1, 1], [2, 2], [0, 2], [1, 1], [2, 0]],
    # M.M
    # .A.
    # S.S
    [[2, 2], [1, 1], [0, 0], [0, 2], [1, 1], [2, 0]],
    # S.M
    # .A.
    # S.M
    [[2, 2], [1, 1], [0, 0], [2, 0], [1, 1], [0, 2]],
    # S.S
    # .A.
    # M.M
]


def check_pattern(x, y, max_x, max_y, grid, pattern) -> bool:
    word = ""
    for i in range(4):
        if (
            x + pattern[i][0] < 0
            or x + pattern[i][0] >= max_x
            or y + pattern[i][1] < 0
            or y + pattern[i][1] >= max_y
        ):
            return False
        word += grid[x + pattern[i][0]][y + pattern[i][1]]
    return word == "XMAS"


def check_cross_pattern(x, y, max_x, max_y, grid, pattern) -> bool:
    word = ""
    for i in range(6):
        if (
            x + pattern[i][0] < 0
            or x + pattern[i][0] >= max_x
            or y + pattern[i][1] < 0
            or y + pattern[i][1] >= max_y
        ):
            return False
        word += grid[x + pattern[i][0]][y + pattern[i][1]]
    return word == "MASMAS"


def part1(file) -> int:
    data: str = read_file(filename=file)
    grid: list[str] = data.split("\n")
    max_row: int = len(grid)
    max_col: int = len(grid[0])
    p1 = 0
    for row in range(max_row):
        for col in range(max_col):
            for pattern in word_patterns:
                if check_pattern(row, col, max_row, max_col, grid, pattern):
                    p1 += 1
    return p1


def part2(file) -> int:
    data: str = read_file(filename=file)
    grid: list[str] = data.split("\n")
    max_row: int = len(grid)
    max_col: int = len(grid[0])
    p2 = 0
    for row in range(max_row):
        for col in range(max_col):
            for pattern in cross_patterns:
                if check_cross_pattern(
                        row, col, max_row, max_col, grid, pattern):
                    p2 += 1
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
    print(f"Part 1: {(secs) / n_iter:.7f} s")


def benchmark_p2(n_iter: int) -> None:
    secs: float = 0
    print("Benchmark 2 -", n_iter, "iterations: ", end=" ")
    for _ in range(n_iter):
        start: float = perf_counter()
        part1(INPUT_FILE)
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
    write_output("./AOC4/output_code.txt")
