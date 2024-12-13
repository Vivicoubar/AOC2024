from time import perf_counter
from typing import NamedTuple
from sys import stdout

EX_FILE: str = "./AOC9/ex1.txt"
INPUT_FILE: str = "./AOC9/input1.txt"


class FileConfig(NamedTuple):
    pos: int
    size: int
    file_id: int


class SpaceConfig(NamedTuple):
    pos: int
    size: int


def read_file(filename) -> str:
    with open(filename, "r") as file:
        return file.read().strip()


def parse_input(
    data: str, part2: bool = False
) -> tuple[list[FileConfig], list[SpaceConfig], list[int | None]]:
    files: list[FileConfig] = []
    spaces: list[SpaceConfig] = []
    disk: list[int | None] = []
    file_id, pos_id = 0, 0
    for i, size_str in enumerate(data):
        size: int = int(size_str)
        if i % 2 == 0:
            # If i is even, it's a file size number
            if part2:
                file_config = FileConfig(pos_id, size, file_id)
                files.append(file_config)
            for i in range(size):
                disk.append(file_id)
                if not part2:
                    file_config = FileConfig(pos_id, 1, file_id)
                    files.append(file_config)
                pos_id += 1
            file_id += 1
        else:  # If i is odd, it's a space size number
            space_config = SpaceConfig(pos_id, size)
            spaces.append(space_config)
            for i in range(size):
                disk.append(None)
                pos_id += 1
    return files, spaces, disk


def order_disk(files, spaces, disk) -> None:
    for file_pos, file_size, file_id in reversed(files):
        for space_i, (space_pos, space_size) in enumerate(spaces):
            if space_pos < file_pos and file_size <= space_size:
                for i in range(file_size):
                    disk[file_pos + i] = None
                    disk[space_pos + i] = file_id
                spaces[space_i] = SpaceConfig(
                    space_pos + file_size, space_size - file_size
                )
                break


def part1and2(file, part2: bool = False) -> int:
    data: str = read_file(file)
    files, spaces, disk = parse_input(data, part2)
    order_disk(files, spaces, disk)
    return checksum(disk)


def checksum(disk) -> int:
    res = 0
    for pos, val in enumerate(disk):
        if val is not None:
            res += pos * val
    return res


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
    benchmark_p1(100)
    benchmark_p2(100)


if __name__ == "__main__":
    show_results()
    write_output("./AOC9/output_code.txt")
