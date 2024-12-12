from time import perf_counter
from sys import stdout
from collections import deque, defaultdict

EX_FILE: str = "./AOC12/ex1.txt"
INPUT_FILE: str = "./AOC12/input1.txt"
MOVEMENTS: list[tuple[int, int]] = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def read_file(filename: str) -> str:
    with open(filename, "r") as file:
        return file.read().strip()


def part1and2(file: str, do_p2: bool = False) -> int:
    data: str = read_file(file)
    grid: list[str] = data.split("\n")
    max_rows: int = len(grid)
    max_cols: int = len(grid[0])
    p1: int = 0
    p2: int = 0
    positions_set = set()
    for row in range(max_rows):
        for col in range(max_cols):
            if (row, col) in positions_set:
                continue
            queue = deque([(row, col)])
            area = 0
            perim = 0
            perim_set = defaultdict(set)
            while queue:
                cur_row, cur_col = queue.popleft()
                if (cur_row, cur_col) in positions_set:
                    continue
                positions_set.add((cur_row, cur_col))
                area += 1
                for movement in MOVEMENTS:
                    new_row = cur_row + movement[0]
                    new_col = cur_col + movement[1]
                    if (
                        0 <= new_row < max_rows
                        and 0 <= new_col < max_cols
                        and grid[new_row][new_col] == grid[cur_row][cur_col]
                    ):
                        # Same letter
                        queue.append((new_row, new_col))
                    else:
                        perim += 1
                        perim_set[movement].add((cur_row, cur_col))
            p1 += area * perim

            if not do_p2:
                continue
            cur_sides: int = 0
            for _, values in perim_set.items():
                seen_perim = set()
                for perim_row, perim_col in values:
                    if (perim_row, perim_col) not in seen_perim:
                        cur_sides += 1
                        queue = deque([(perim_row, perim_col)])
                        while queue:
                            new_perim_row, new_perim_col = queue.popleft()
                            if (new_perim_row, new_perim_col) in seen_perim:
                                continue
                            seen_perim.add((new_perim_row, new_perim_col))
                            for movement in MOVEMENTS:
                                new_row = new_perim_row + movement[0]
                                new_col = new_perim_col + movement[1]
                                if (new_row, new_col) in values:
                                    queue.append((new_row, new_col))
            p2 += area * cur_sides
    return p1 if not do_p2 else p2


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
    write_output("./AOC12/output.txt")
