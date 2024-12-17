from sys import stdout
import heapq as priority_queue
from time import perf_counter

AVAILABLE_DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # up right down left

EX_FILE = "./AOC16/ex1.txt"
INPUT_FILE = "./AOC16/input1.txt"


def read_file(file):
    return open(file).read().strip()


def calc_optimal_nodes(seen, distances, distances_reverse, best_path):
    optimal_nodes = set()
    for row, col, _ in seen:
        for direction in range(4):
            if (
                (row, col, direction) in distances
                and (row, col, direction) in distances_reverse
                and distances[(row, col, direction)]
                + distances_reverse[(row, col, direction)]
                == best_path
            ):
                optimal_nodes.add((row, col))
    return optimal_nodes


def part1and2(file):
    grid = read_file(file).split("\n")
    max_row = len(grid)
    max_col = len(grid[0])
    grid = [[grid[row][col]
             for col in range(max_col)] for row in range(max_row)]
    start_row, start_col = 0, 0
    end_row, end_col = 0, 0
    for row in range(max_row):
        for col in range(max_col):
            if grid[row][col] == "S":
                start_row, start_col = row, col
            if grid[row][col] == "E":
                end_row, end_col = row, col

    queue = []
    seen_nodes = set()
    priority_queue.heappush(queue, (0, start_row, start_col, 1))
    distances = {}
    best_path = None
    while queue:
        distance, row, col, direction = priority_queue.heappop(queue)
        if (row, col, direction) not in distances:
            distances[(row, col, direction)] = distance
        if row == end_row and col == end_col and best_path is None:
            best_path = distance
        if (row, col, direction) in seen_nodes:
            continue
        seen_nodes.add((row, col, direction))
        row_dir, col_dir = AVAILABLE_DIRS[direction]
        new_row, new_col = row + row_dir, col + col_dir
        if (
            0 <= new_col < max_col
            and 0 <= new_row < max_row
            and grid[new_row][new_col] != "#"
        ):
            priority_queue.heappush(
                queue, (distance + 1, new_row, new_col, direction))
        priority_queue.heappush(
            queue, (distance + 1000, row, col, (direction + 1) % 4))
        priority_queue.heappush(
            queue, (distance + 1000, row, col, (direction + 3) % 4))
    reverse_queue = []
    seen_nodes_reverse = set()
    for direction in range(4):
        priority_queue.heappush(
            reverse_queue, (0, end_row, end_col, direction))
    distances_reverse = {}
    while reverse_queue:
        distance, row, col, direction = priority_queue.heappop(reverse_queue)
        if (row, col, direction) not in distances_reverse:
            distances_reverse[(row, col, direction)] = distance
        if (row, col, direction) in seen_nodes_reverse:
            continue
        seen_nodes_reverse.add((row, col, direction))
        row_dir, col_dir = AVAILABLE_DIRS[(direction + 2) % 4]
        new_row, new_col = row + row_dir, col + col_dir
        if (
            0 <= new_col < max_col
            and 0 <= new_row < max_row
            and grid[new_row][new_col] != "#"
        ):
            priority_queue.heappush(
                reverse_queue, (distance + 1, new_row, new_col, direction)
            )
        priority_queue.heappush(
            reverse_queue, (distance + 1000, row, col, (direction + 1) % 4)
        )
        priority_queue.heappush(
            reverse_queue, (distance + 1000, row, col, (direction + 3) % 4)
        )

    optimal_nodes = calc_optimal_nodes(
        seen_nodes, distances, distances_reverse, best_path
    )
    return best_path, len(optimal_nodes)


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
        part1and2(INPUT_FILE)
        end: float = perf_counter()
        secs += end - start
        print(".", end=" ")
        stdout.flush()
    print(f"Part 2: {(secs) / n_iter:.7f} s")


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
    benchmark_p1(20)
    benchmark_p2(20)


if __name__ == "__main__":
    show_results()
    write_output("./AOC16/output_code.txt")
