from time import perf_counter

EX_FILE: str = "./AOC7/ex1.txt"
INPUT_FILE: str = "./AOC7/input1.txt"


def read_file(filename) -> str:
    with open(filename, "r") as file:
        return file.read().strip()


def can_get_res(target: str, numbers: list[int], p2: bool) -> bool:
    # We use a recursive function to check if we can get the target number
    if len(numbers) == 1:
        return numbers[0] == int(target)
    if can_get_res(
        target, [numbers[0] + numbers[1]] + numbers[2:], p2
    ):  # We add the first two numbers and check if we can get the target number
        return True
    if can_get_res(
        target, [numbers[0] * numbers[1]] + numbers[2:], p2
    ):  # We multiply the first two numbers and check if we can get the target number
        return True
    if p2 and can_get_res(
        target, [int(str(numbers[0]) + str(numbers[1]))] + numbers[2:], p2
    ):  # We concatenate the first two numbers and check if we can get the target number
        return True
    return False


def part1and2(file) -> tuple[int, int]:
    lines: list[str] = read_file(file).strip().split("\n")
    res_1: int = 0
    res_2: int = 0
    for line in lines:
        expected_res, num_str = line.split(": ")
        numbers = list(map(int, num_str.split()))
        if can_get_res(expected_res, numbers, False):
            res_1 += int(expected_res)
        if can_get_res(expected_res, numbers, True):
            res_2 += int(expected_res)
    return res_1, res_2


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
    write_output("./AOC7/output_code.txt")
