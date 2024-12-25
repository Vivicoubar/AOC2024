from time import perf_counter
from sys import stdout

EX_FILE = "./AOC25/ex1.txt"
INPUT_FILE = "./AOC25/input1.txt"
DIRS: list[tuple[int, int]] = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def read_file(file):
    with open(file, "r") as f:
        return f.read().strip()


def try_key(key, lock) -> bool:
    max_rows = len(key)
    max_col = len(key[0])
    for row in range(max_rows):
        for col in range(max_col):
            if key[row][col] == "#" and lock[row][col] == "#":
                return False
    return True


def part1(file):
    data = read_file(file)
    doors = data.split("\n\n")
    keys = []
    locks = []
    for door in doors:
        grid = door.split("\n")
        max_row = len(grid)
        max_col = len(grid[0])
        grid = [[grid[row][col]
                 for col in range(max_col)] for row in range(max_row)]
        is_valid = True
        for col in range(max_col):
            if grid[0][col] == "#":
                is_valid = False
        if is_valid:
            keys.append(door)
        else:
            locks.append(door)
    p1 = 0
    for key in keys:
        for lock in locks:
            if try_key(key, lock):
                p1 += 1
    return p1


def benchmark_p1(n_iter: int) -> None:
    secs: float = 0
    print("Benchmark 1-", n_iter, "iterations: ", end=" ")
    for _ in range(n_iter):
        start: float = perf_counter()
        part1(INPUT_FILE)
        end: float = perf_counter()
        secs += end - start
        print(".", end=" ")
        stdout.flush()
    print(f"Part 1:{(secs) / n_iter:.7f} s")


def write_output(output_file):
    res_1 = part1(INPUT_FILE)
    with open(output_file, "w") as f:
        # Real Input results
        f.write(f"{res_1}\n")


def show_results():
    res_1 = part1(INPUT_FILE)
    print("----- [Results] -----")
    print("Res 1: " + str(res_1))
    print("--- [Benchmarks] ---")
    benchmark_p1(20)


if __name__ == "__main__":
    show_results()
    write_output("./AOC25/output_code.txt")
