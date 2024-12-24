from time import perf_counter
from sys import stdout
from heapq import heappop, heappush
import re
from typing import NamedTuple

EX_FILE = "./AOC21/ex1.txt"
INPUT_FILE = "./AOC21/input1.txt"

first_pad = ["789", "456", "123", " 0A"]
second_pad = [" ^A", "<v>"]
buttons = ["^", "<", "v", ">", "A"]


class Data(NamedTuple):
    dist: int
    pos1: tuple[int, int]
    pos2: str
    out: str
    path: str


class State(NamedTuple):
    pos1: tuple[int, int]
    pos2: str
    out: str


class Move(NamedTuple):
    button_label: str
    cur_mov: str
    pads: int


def read_file(file):
    with open(file) as f:
        return f.read().strip()


def ints(s):
    return [int(x) for x in re.findall(r"-?\d+", s)]


def get_pad1_button(pos) -> str:
    r, c = pos
    if not (0 <= r < len(first_pad) and 0 <= c < len(first_pad[r])):
        return ""
    if first_pad[r][c] == " ":
        return ""
    return first_pad[r][c]


def get_pad2_button(pos) -> str:
    r, c = pos
    if not (0 <= r < len(second_pad) and 0 <= c < len(second_pad[r])):
        return ""
    if second_pad[r][c] == " ":
        return ""
    return second_pad[r][c]


def move_pad1(pos: tuple[int, int], move) -> tuple[tuple[int, int], str]:
    if move == "A":
        return (pos, get_pad1_button(pos))
    elif move == "<":
        return ((pos[0], pos[1] - 1), "")
    elif move == "^":
        return ((pos[0] - 1, pos[1]), "")
    elif move == ">":
        return ((pos[0], pos[1] + 1), "")
    elif move == "v":
        return ((pos[0] + 1, pos[1]), "")
    else:
        raise ValueError(f"Invalid move {move}")


def move_pad2(pos, move) -> tuple[tuple[int, int], str]:
    if move == "A":
        return (pos, get_pad2_button(pos))
    elif move == "<":
        return ((pos[0], pos[1] - 1), "")
    elif move == "^":
        return ((pos[0] - 1, pos[1]), "")
    elif move == ">":
        return ((pos[0], pos[1] + 1), "")
    elif move == "v":
        return ((pos[0] + 1, pos[1]), "")
    else:
        raise ValueError(f"Invalid move {move}")


def priotity_search(code, pads) -> int:
    start: Data = Data(0, (3, 2), "A", "", "")
    queue: list[Data] = []
    heappush(queue, start)
    states: dict[State, int] = {}
    while queue:
        dist, pos1, pos2, out, path = heappop(queue)
        if out == code:
            return dist
        if not code.startswith(out):
            continue
        if get_pad1_button(pos1) == "":
            continue
        state = State(pos1, pos2, out)
        if state in states:
            continue
        states[state] = dist
        for button in buttons:
            new_pos1, output = move_pad1(pos1, button)
            new_out = out if output == "" else out + output
            cost_move = cost_pad2(button, pos2, pads)
            heappush(
                queue,
                Data(
                    dist +
                    cost_move,
                    new_pos1,
                    button,
                    new_out,
                    path))
    return -1


DYNAMIC_PROG_DICT: dict[Move, int] = {}


def cost_pad2(button_label, cur_mov, pads) -> int:
    start_positions: dict[str, tuple[int, int]] = {
        "^": (0, 1),
        "<": (1, 0),
        "v": (1, 1),
        ">": (1, 2),
        "A": (0, 2),
    }
    state: Move = Move(button_label, cur_mov, pads)
    if state in DYNAMIC_PROG_DICT:
        return DYNAMIC_PROG_DICT[state]
    if pads == 0:
        return 1
    else:
        queue: list[Data] = []
        start_pos = start_positions[cur_mov]
        heappush(queue, Data(0, start_pos, "A", "", ""))
        seen_positions = {}
        while queue:
            dist, pos1, pos2, out, path = heappop(queue)
            if get_pad2_button(pos1) == "":
                continue
            if out == button_label:
                DYNAMIC_PROG_DICT[state] = dist
                return dist
            elif len(out) > 0:
                continue
            positions = (pos1, pos2)
            if positions in seen_positions:
                continue
            seen_positions[positions] = dist
            for button in buttons:
                new_pos, output = move_pad2(pos1, button)
                cost = cost_pad2(button, pos2, pads - 1)
                new_dist = dist + cost
                new_out = out if output == "" else out + output
                heappush(queue, Data(new_dist, new_pos, button, new_out, path))
        return -1


def part1and2(file) -> tuple[int, int]:
    p1 = 0
    p2 = 0
    DYNAMIC_PROG_DICT.clear()
    for line in read_file(file).split("\n"):
        s1: int = priotity_search(line, 2)
        s2: int = priotity_search(line, 25)
        line_int: int = ints(line)[0]
        p1 += line_int * s1
        p2 += line_int * s2
    return p1, p2


def benchmark_p1and2(n_iter: int) -> None:
    secs: float = 0
    print("Benchmark 1 & 2 -", n_iter, "iterations: ", end=" ")
    for _ in range(n_iter):
        start: float = perf_counter()
        part1and2(INPUT_FILE)
        end: float = perf_counter()
        secs += end - start
        print(".", end=" ")
        stdout.flush()
    print(f"Part 1 & 2 :{(secs) / n_iter:.7f} s")


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
    write_output("./AOC21/output_code.txt")
