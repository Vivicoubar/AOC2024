from time import perf_counter
from sys import stdout

EX_FILE: str = "./AOC6/ex1.txt"
INPUT_FILE: str = "./AOC6/input1.txt"


def read_file(filename) -> str:
    with open(filename, "r") as file:
        return file.read().strip()


def is_out_of_bounds(x: int, y: int, max_x: int, max_y: int) -> bool:
    return x < 0 or x >= max_x or y < 0 or y >= max_y


def calc_next_pos(
    x: int, y: int, dir_mov: list[list[int]], dir_ind: int
) -> tuple[int, int]:
    return x + dir_mov[dir_ind][0], y + dir_mov[dir_ind][1]


def get_guard_coords(data: list[str]) -> tuple[int, int]:
    for x in range(len(data)):
        for y in range(len(data[0])):
            if data[x][y] == "^":
                return x, y
    return 0, 0


def get_next_pos(x: int,
                 y: int,
                 dir_m: list[list[int]],
                 dir_i: int) -> tuple[int,
                                      int]:
    return x + dir_m[dir_i][0], y + dir_m[dir_i][1]


def do_loop(
    data, max_loop, dir_mov, dir_i, box_x, box_y
) -> tuple[set[tuple[int, int]], bool]:
    guard_coords: tuple[int, int] = get_guard_coords(data)
    seen_pos: set[tuple[int, int]] = set()
    seen_pos_dir: set[tuple[int, int, int]] = set()
    seen_pos.add((guard_coords[0], guard_coords[1]))
    seen_pos_dir.add((guard_coords[0], guard_coords[1], dir_i))
    max_iter: int = max_loop
    cur_iter: int = 0
    while cur_iter < max_iter:
        cur_iter += 1
        next_pos: tuple[int, int] = get_next_pos(
            guard_coords[0], guard_coords[1], dir_mov, dir_i
        )
        x, y = next_pos
        # Check if the next position is out of bounds (Part 1)
        if is_out_of_bounds(x, y, len(data), len(data[0])):
            return seen_pos, False
        # Check if the next position is a loop (Part 2)
        if (x, y, dir_i) in seen_pos_dir:
            return seen_pos, True
        # Update the seen positions and the guard coordinates
        if data[x][y] == "#" or next_pos == (box_x, box_y):
            dir_i = (dir_i + 1) % 4
            continue
        guard_coords = next_pos
        seen_pos.add((x, y))
        seen_pos_dir.add((x, y, dir_i))
    return set(), False


def part1and2(file, only1: bool = False) -> tuple[int, int]:
    data: list[str] = read_file(filename=file).split("\n")
    max_loop: int = len(data) * len(data[0]) * 10
    dir_mov: list[list[int]] = [[-1, 0], [0, 1], [1, 0], [0, -1]]
    dir_ind: int = 0
    seen_pos, _ = do_loop(data, max_loop, dir_mov, dir_ind, -1, -1)
    res1: int = len(seen_pos)
    res2: int = 0
    if only1:
        return res1, 0
    # --- [Part 2] ---
    for pos in seen_pos:
        _, is_loop = do_loop(data, max_loop, dir_mov, dir_ind, pos[0], pos[1])
        if is_loop:
            res2 += 1
    return res1, res2


def benchmark_p1and2(n_iter: int) -> None:
    secs: float = 0
    print("Benchmark 1 and 2 -", n_iter, "iterations: ", end=" ")
    for _ in range(n_iter):
        start: float = perf_counter()
        part1and2(INPUT_FILE)
        end: float = perf_counter()
        secs += end - start
        print(".", end=" ")
        stdout.flush()
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
    benchmark_p1and2(20)


if __name__ == "__main__":
    show_results()
    write_output("./AOC6/output_code.txt")
