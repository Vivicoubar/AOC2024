from collections import defaultdict
from time import perf_counter

EX_FILE: str = "./AOC5/ex1.txt"
INPUT_FILE: str = "./AOC5/input1.txt"


def read_file(filename) -> str:
    with open(filename, "r") as file:
        return file.read().strip()


def part1and2() -> tuple[int, int]:
    data: str = read_file(filename=INPUT_FILE)
    entry, queries = data.split("\n\n")
    before_x: dict[int, set[int]] = defaultdict(set)
    after_x: dict[int, set[int]] = defaultdict(set)
    res1 = 0
    res2 = 0
    for line in entry.split("\n"):
        x, y = map(int, line.split("|"))
        before_x[y].add(x)
        after_x[x].add(y)
    for query in queries.split("\n"):
        line = list(map(int, query.split(",")))
        is_good_line = True
        for i, x in enumerate(line):
            for j, y in enumerate(line):
                # If y must come before x, then the line is not good
                if i < j and y in before_x[x]:
                    is_good_line = False
        if is_good_line:
            res1 += line[len(line) // 2]
        else:
            good: list[int] = sort_line(line, before_x, after_x)
            res2 += good[len(good) // 2]
    return res1, res2


def sort_line(
    line: list[int], before_x: dict[int, set[int]], after_x: dict[int, set[int]]
) -> list[int]:
    good: list[int] = []
    # Element in the list with the number of dependencies as the number of
    # elements that must come before it
    dependencies: dict[int, int] = {
        element: len(before_x[element] & set(line)) for element in line
    }
    queue: list[int] = [
        element for element in line if dependencies[element] == 0]
    # Add elements that have no dependencies to the queue to start the process
    # We do a topological sort
    while queue:
        x: int = queue.pop(0)
        # Remove the first element of the queue, because its dependencies are
        # resolved
        good.append(x)
        for y in after_x[x]:
            # For each element that must come after x, we decrement its
            # dependencies, and if it reaches 0, we add it to the queue
            if y in dependencies:
                dependencies[y] -= 1
                if dependencies[y] == 0:
                    queue.append(y)
    return good


def benchmark_p1and2(n_iter: int) -> None:
    secs: float = 0
    for _ in range(n_iter):
        start: float = perf_counter()
        part1and2()
        end: float = perf_counter()
        secs += end - start
    print(f"Part 1 and 2: {(secs) / n_iter:.7f} s")


res_1, res_2 = part1and2()
print("----- [Results] -----")
print("Res 1: " + str(res_1))
print("Res 2: " + str(res_2))
print("--- [Benchmarks] ---")
benchmark_p1and2(100)
