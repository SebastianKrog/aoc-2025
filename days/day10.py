from __future__ import annotations

from typing import Any
#from z3 import Int, Optimize, Sum, sat

from re import findall
from itertools import product
from functools import cache, reduce
from operator import xor

from aoc.search import bfs_one

from aoc.common import read_input, time_call
from aoc.config import AOC_YEAR

DAY = 10


def parse_input(raw: str) -> Any:
    """Convert the raw text into a convenient structure."""
    input = raw.rstrip("\n").splitlines()
    re = r"^\[([.#]+)\] (\(.+\)) \{(.+)\}$"
    machines = [findall(re, l)[0] for l in input]
    out = []
    for lights, buttons, joltage in machines:
        lights = [c == "#" for c in lights]
        buttons = tuple(tuple(int(a) for a in l.strip("()").split(","))
                   for l in findall(r"\([0-9,]+\)", buttons))
        joltage = tuple(int(a) for a in  joltage.split(","))
        out.append((lights, buttons, joltage))
    return out


def part1(data: Any) -> Any:
    """Solve part 1."""
    # Recompute for modulo math
    machines = []
    for lights, bts, _ in data:
        lights = sum(l*(2**n) for n, l in enumerate(lights))
        bts = [sum(2**n for n in b) for b in bts]
        machines.append((lights, bts))

    def fewest_presses(lights, bts):
        return bfs_one(
            start=0,
            neighbors=lambda l: [l^btn for btn in bts],
            is_goal=lambda x: x == lights
        ).goal_cost()

    return sum(fewest_presses(l,b) for l,b in machines) 


def part2(data: Any) -> Any:
    """Solve part 2."""

    def fewest_presses(data_row):
        _, buttons, joltages = data_row
        m_bts = tuple(sum(2**n for n in b) for b in buttons)

        parity_map = {i: set() for i in range(2**len(joltages))}
        for push_combination in product([0, 1], repeat=len(buttons)):
            m_par = reduce(xor, (x for x, push in zip(m_bts, push_combination) if push), 0)
            parity_map[m_par].add(push_combination)

        @cache
        def _fewest_presses(joltages):
            if any(j < 0 for j in joltages): return 10**8
            if all(j == 0 for j in joltages): return 0

            m_par = sum((j & 1) << n for n, j in enumerate(joltages))
            solutions = parity_map[m_par]

            if len(solutions) == 0: return 10**8

            next = []
            for pushes in solutions:
                new_joltages = list(joltages)
                for btn, push in zip(buttons, pushes):
                    if push:
                        for j in btn: new_joltages[j] -= 1
                next.append((tuple(j//2 for j in new_joltages), sum(pushes)))

            return min(p + 2 * _fewest_presses(nj) for nj, p in next)
        
        return _fewest_presses(joltages)

    return sum(map(fewest_presses, data))


# def solve_z3(data_row):
#     _, buttons, joltages = data_row
#     # For each joltage dial, find the buttons that can manipulate it
#     j_bts = [[] for i, _ in enumerate(joltages)]

#     for i, btn in enumerate(buttons):
#         for dial in btn:
#             j_bts[dial].append(i)

#     # We use Z3
#     # Define vars using Int(x_i), one for each button
#     vars = [Int(f"x{i}") for i, _ in enumerate(buttons)]

#     # Initialize the solver
#     solver = Optimize()

#     # Add assumptions (x_i >= 0)
#     solver.add([v >= 0 for v in vars])

#     # Add an equation for each dial D (D_j == x_j0 ... x_jn)
#     for j, dial_setting in enumerate(joltages):
#         solver.add(Sum([vars[i] for i in j_bts[j]]) == dial_setting)

#     # Find the solution that minimizes the sum of vars
#     solver.minimize(Sum(vars))

#     if solver.check() != sat:
#         raise RuntimeError("No solution found")
    
#     model = solver.model()

#     #print([model.evaluate(v).as_long() for v in vars]) # Print button presses
#     return int(model.evaluate(Sum(vars)).as_long())


def main() -> None:
    p1 = time_call(lambda x: part1(parse_input(x)), read_input(DAY))
    print(f"{AOC_YEAR} Day {DAY} - Part 1: {p1.value} ({p1.seconds:.3f}s)")

    p2 = time_call(lambda x: part2(parse_input(x)), read_input(DAY))
    print(f"{AOC_YEAR} Day {DAY} - Part 2: {p2.value} ({p2.seconds:.3f}s)")


if __name__ == "__main__":
    main()
