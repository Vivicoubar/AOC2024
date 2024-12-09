from time import perf_counter
from collections import defaultdict

EX_FILE: str = "./AOC8/ex1.txt"
INPUT_FILE: str = "./AOC8/input1.txt"


def read_file(filename) -> str:
    with open(filename, "r") as file:
        return file.read().strip()


def part1and2(file) -> tuple[int, int]:
    grid: list[str] = read_file(file).strip().split("\n")
    set_part1: set[tuple[int, int]] = set()
    set_part2: set[tuple[int, int]] = set()
    rows: int = len(grid)
    cols: int = len(grid[0])
    points: defaultdict = defaultdict(list)
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] != ".":
                points[grid[row][col]].append((row, col))
    for row in range(rows):
        for col in range(cols):
            for _, values in points.items():
                for point1_row, point1_col in values:
                    for point2_row, point2_col in values:
                        if (point1_row, point1_col) != (
                                point2_row, point2_col):
                            # If three points are in the same line, two lines
                            # from any point to the others have the same slope
                            dist1 = abs(row - point1_row) + \
                                abs(col - point1_col)
                            delta_row1 = row - point1_row
                            delta_col1 = col - point1_col
                            dist2 = abs(row - point2_row) + \
                                abs(col - point2_col)
                            delta_row2 = row - point2_row
                            delta_col2 = col - point2_col
                            if (0 <= row < rows and 0 <= col < cols and (
                                    delta_row1 * delta_col2 == delta_col1 * delta_row2)):
                                if dist1 == 2 * dist2 or dist1 * 2 == dist2:
                                    set_part1.add((row, col))
                                set_part2.add((row, col))
    return len(set_part1), len(set_part2)


def benchmark_p1and2(n_iter: int) -> None:
    secs: float = 0
    for _ in range(n_iter):
        start: float = perf_counter()
        part1and2(INPUT_FILE)
        end: float = perf_counter()
        secs += end - start
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
    benchmark_p1and2(100)


if __name__ == "__main__":
    # show_results()
    write_output("./AOC8/output_code.txt")
