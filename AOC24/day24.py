from time import perf_counter
from sys import stdout
from collections import defaultdict, deque, Counter
import operator as op

EX_FILE = "./AOC24/ex1.txt"
INPUT_FILE = "./AOC24/input1.txt"

SWAPS = []
GATES = {}


def read_file(file):
    with open(file, "r") as f:
        return f.read().strip()


def find_rule(wire1, operation, wire2):
    for output_wire, (w1, operator, w2) in GATES.items():
        if (wire1, operation, wire2) in [
                (w1, operator, w2), (w2, operator, w1)]:
            return output_wire
    return None


def swap(wire1, wire2):
    global SWAPS
    GATES[wire1], GATES[wire2] = GATES[wire2], GATES[wire1]
    SWAPS += [wire1, wire2]


def topological_sort(wires, edges):
    """
    Perform a topological sort of the wires based on the given dependency graph (edges).

    Args:
        wires (list): List of all wires (nodes) in the graph.
        edges (dict): A defaultdict where keys are nodes and values are lists of dependent nodes.

    Returns:
        list: A topologically sorted list of wires.
    """
    sorted_wires = []
    in_degree = Counter()

    # Calculate in-degrees for each node
    for wire in wires:
        for wire_to in edges[wire]:
            in_degree[wire_to] += 1

    # Initialize the stack with nodes having zero in-degree
    stack = deque([wire for wire in wires if in_degree[wire] == 0])

    # Perform topological sort
    while stack:
        wire = stack.popleft()
        sorted_wires.append(wire)
        for wire_to in edges[wire]:
            in_degree[wire_to] -= 1
            if in_degree[wire_to] == 0:
                stack.append(wire_to)

    # Ensure all wires are sorted
    if len(sorted_wires) != len(wires):
        raise ValueError("Graph contains cycles or disconnected components.")

    return sorted_wires


def part1and2(file):
    blocks = [block.splitlines() for block in read_file(file).split("\n\n")]
    OPERATORS = {"AND": op.and_, "OR": op.or_, "XOR": op.xor}
    inputs = {}
    for line in blocks[0]:
        x, y = line.split(": ")
        inputs[x] = int(y)

    sides = defaultdict(list)
    for line in blocks[1]:
        left, wire_out = line.split(" -> ")
        wire_in_1, operator, wire_in_2 = left.split()
        GATES[wire_out] = (wire_in_1, operator, wire_in_2)
        sides[wire_in_1] += [wire_out]
        sides[wire_in_2] += [wire_out]
    wires = list(inputs.keys()) + list(GATES.keys())
    goal_wires = sorted(
        (wire for wire in wires if wire.startswith("z")),
        reverse=True)
    sorted_wires = topological_sort(wires, sides)
    outputs = {}
    for wire in sorted_wires:
        if wire in inputs:
            outputs[wire] = inputs[wire]
        else:
            wire1, operator, wire2 = GATES[wire]
            outputs[wire] = OPERATORS[operator](outputs[wire1], outputs[wire2])
    binary_result = "".join(map(str, [outputs[wire] for wire in goal_wires]))
    p1 = int(binary_result, 2)
    # P2
    gate_and = [None] * 45
    gate_xor = [None] * 45
    gate_z = [None] * 45
    gate_tmp = [None] * 45
    gate_carry = [None] * 45
    i = 0
    x = f"x{str(i).zfill(2)}"
    y = f"y{str(i).zfill(2)}"
    gate_and[i] = find_rule(x, "AND", y)
    gate_xor[i] = find_rule(x, "XOR", y)
    gate_z[i] = gate_xor[i]
    gate_carry[i] = gate_and[i]
    for i in range(1, 45):
        x = f"x{str(i).zfill(2)}"
        y = f"y{str(i).zfill(2)}"
        z = f"z{str(i).zfill(2)}"
        is_valid = True
        while is_valid:
            is_valid = False
            gate_xor[i] = find_rule(x, "XOR", y)
            gate_and[i] = find_rule(x, "AND", y)
            w1, operator, w2 = GATES[z]
            if w1 == gate_carry[i - 1] and w2 != gate_xor[i]:
                swap(w2, gate_xor[i])
                is_valid = True
                continue
            if w2 == gate_carry[i - 1] and w1 != gate_xor[i]:
                swap(w1, gate_xor[i])
                is_valid = True
                continue
            gate_z[i] = find_rule(gate_xor[i], "XOR", gate_carry[i - 1])
            if gate_z[i] != z:
                swap(gate_z[i], z)
                is_valid = True
                continue

            gate_tmp[i] = find_rule(gate_xor[i], "AND", gate_carry[i - 1])
            gate_carry[i] = find_rule(gate_tmp[i], "OR", gate_and[i])
    p2 = ",".join(sorted(SWAPS))
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
    res_1, res_2 = part1and2(INPUT_FILE)
    with open(output_file, "w") as f:
        # Real Input results
        f.write(f"{res_1}\n")
        f.write(f"{res_2}\n")


def show_results():
    res_1, res_2 = part1and2(INPUT_FILE)
    print("----- [Results] -----")
    print("Res 1: " + str(res_1))
    print("Res 2: " + str(res_2))
    print("--- [Benchmarks] ---")
    benchmark_p1and2(20)


if __name__ == "__main__":
    show_results()
    write_output("./AOC24/output_code.txt")
