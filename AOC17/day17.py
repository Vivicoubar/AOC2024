from time import perf_counter
from sys import stdout


EX_FILE: str = "./AOC17/ex1.txt"
INPUT_FILE: str = "./AOC17/input1.txt"
EX2_FILE: str = "./AOC17/ex2.txt"


def read_file(file: str) -> str:
    with open(file, "r") as f:
        return f.read().strip()


def part1(file: str) -> str:
    data = read_file(file).split("\n")
    reg_a = int(data[0].split(" ")[-1])
    reg_b, reg_c = 0, 0
    i = 0
    w = []
    program = list(map(int, data[4].split(": ")[1].split(",")))
    while i < len(program):
        # Operand
        if program[i + 1] <= 3:
            operand = program[i + 1]
        elif program[i + 1] == 4:
            operand = reg_a
        elif program[i + 1] == 5:
            operand = reg_b
        elif program[i + 1] == 6:
            operand = reg_c
        else:
            operand = 0
        # Operations
        # adv -> Division by 2^operand, whcih is the same as shifting right by
        # operand
        if program[i] == 0:
            reg_a >>= operand
        # bxl -> Bitwise XOR with literal operand (so we don't use operand)
        elif program[i] == 1:
            reg_b ^= program[i + 1]
        # bst -> Calculate the operand modulo 8 and store it in reg_b
        elif program[i] == 2:
            reg_b = operand & 7
        # jnz -> Jump if reg_a is not 0
        elif program[i] == 3:
            i = program[i + 1] - 2 if reg_a != 0 else i
        # bxc -> Bitwise XOR between reg_b and reg_c (no need to use operand)
        elif program[i] == 4:
            reg_b ^= reg_c
        # out -> Output operand modulo 8
        elif program[i] == 5:
            w.append(operand & 7)
        # bdv -> Bitwise division between reg_a and operand stored in reg_b
        elif program[i] == 6:
            reg_b = reg_a >> operand
        # cdv -> Bitwise division between reg_a and operand stored in reg_c
        elif program[i] == 7:
            reg_c = reg_a >> operand
        # Increment i by 2
        i += 2
    return ",".join(map(str, w))


def part2(file: str) -> int:
    data = read_file(file).split("\n")
    # Find A
    program = list(map(int, data[4].split(": ")[1].split(",")))
    global output
    output = 0

    def solve(pointer, r):
        if pointer < 0:
            global output
            output = r
            return True
        reg_b, reg_c = 0, 0
        solv_output = 0
        for digit in range(8):
            reg_a, i = r << 3 | digit, 0
            while i < len(program):
                # Operand
                if program[i + 1] <= 3:
                    operand = program[i + 1]
                elif program[i + 1] == 4:
                    operand = reg_a
                elif program[i + 1] == 5:
                    operand = reg_b
                elif program[i + 1] == 6:
                    operand = reg_c
                else:
                    operand = 0
                # Operations
                # adv -> Division by 2^operand, whcih is the same as shifting
                # right by operand
                if program[i] == 0:
                    reg_a >>= operand
                # bxl -> Bitwise XOR with literal operand (so we don't use
                # operand)
                elif program[i] == 1:
                    reg_b ^= program[i + 1]
                # bst -> Calculate the operand modulo 8 and store it in reg_b
                elif program[i] == 2:
                    reg_b = operand & 7
                # jnz -> Jump if reg_a is not 0
                elif program[i] == 3:
                    i = program[i + 1] - 2 if reg_a != 0 else i
                # bxc -> Bitwise XOR between reg_b and reg_c (no need to use
                # operand)
                elif program[i] == 4:
                    reg_b ^= reg_c
                # out -> Output operand modulo 8
                elif program[i] == 5:
                    solv_output = operand & 7
                    break
                # bdv -> Bitwise division between reg_a and operand stored in
                # reg_b
                elif program[i] == 6:
                    reg_b = reg_a >> operand
                # cdv -> Bitwise division between reg_a and operand stored in
                # reg_c
                elif program[i] == 7:
                    reg_c = reg_a >> operand
                # Increment i by 2
                i += 2
            if solv_output == program[pointer] and solve(
                    pointer - 1, r << 3 | digit):
                return True
        return False

    solve(len(program) - 1, 0)
    return output


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
    res_ex1, res_ex2 = part1(EX_FILE), part2(EX2_FILE)
    res_1, res_2 = part1(INPUT_FILE), part2(INPUT_FILE)
    # Write the output in the format required (4 lines)
    with open(output_file, "w") as f:
        # Example Input results
        f.write(f"{res_ex1}\n")
        f.write(f"{res_ex2}\n")
        # Real Input results
        f.write(f"{res_1}\n")
        f.write(f"{res_2}\n")


def show_results():
    res_ex1, res_ex2 = part1(EX_FILE), part2(EX2_FILE)
    res_1, res_2 = part1(INPUT_FILE), part2(INPUT_FILE)
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
    write_output("./AOC17/output_code.txt")
