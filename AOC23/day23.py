from sys import stdout
from time import perf_counter
from collections import defaultdict

EX_FILE = "./AOC23/ex1.txt"
INPUT_FILE = "./AOC23/input1.txt"


def read_file(file):
    with open(file, "r") as f:
        return f.read().strip()


def part1(file):
    p1 = 0
    data = read_file(file)
    elements = defaultdict(set)
    for line in data.split("\n"):
        a, b = line.split("-")
        elements[a].add(b)
        elements[b].add(a)
    computers = sorted(elements.keys())
    for i, a in enumerate(computers):
        for j in range(i + 1, len(computers)):
            for k in range(j + 1, len(computers)):
                b = computers[j]
                c = computers[k]
                if a in elements[b] and a in elements[c] and b in elements[c]:
                    if a.startswith("t") or b.startswith(
                            "t") or c.startswith("t"):
                        p1 += 1
    return p1


def part2(file):
    data = read_file(file)
    elements = defaultdict(set)
    for line in data.split("\n"):
        a, b = line.split("-")
        elements[a].add(b)
        elements[b].add(a)
    computers = sorted(elements.keys())
    best = []
    for t in range(1000):
        clique = []
        for x in computers:
            ok = True
            for y in clique:
                if x not in elements[y]:
                    ok = False
            if ok:
                clique.append(x)
        if best is None or len(clique) > len(best):
            best = clique
    sorted_best = sorted(best)
    return (",").join(sorted_best)


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
    res_ex1: int = part1(EX_FILE)
    res_ex2: str = part2(EX_FILE)
    res_1: int = part1(INPUT_FILE)
    res_2: str = part2(INPUT_FILE)
    # Write the output in the format required (4 lines)
    with open(output_file, "w") as f:
        # Example Input results
        f.write(f"{res_ex1}\n")
        f.write(f"{res_ex2}\n")
        # Real Input results
        f.write(f"{res_1}\n")
        f.write(f"{res_2}\n")


def show_results():
    res_ex1: int = part1(EX_FILE)
    res_ex2: str = part2(EX_FILE)
    res_1: int = part1(INPUT_FILE)
    res_2: str = part2(INPUT_FILE)
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
    write_output("./AOC23/output_code.txt")
