from __future__ import annotations

from typing import Any
from z3 import Int, Optimize, Sum, sat

from re import findall
#from itertools import combinations, permutations, product
#from math import prod, lcm, ceil, floor, gcd

from aoc.progress import prog # Add a progress bar when needed (used as enumerate)

#from aoc.grid import NORTH, SOUTH, EAST, WEST, DIR4, neighbors4, parse_char_grid,
#  parse_int_grid, add_pos, UP, DOWN, LEFT, RIGHT, in_bounds
#from aoc.grid import NORTH, SOUTH, EAST, WEST, DIR8, neighbors8, parse_char_grid,
#  NORTH_EAST as NE, NORTH_WEST as NW, SOUTH_EAST as SE, SOUTH_WEST as SW
from aoc.search import bfs_one, dijkstra_one
#from aoc.iteration import split_by, unique_permutations, nwise

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
        buttons = tuple((int(a) for a in l.strip("()").split(","))
                   for l in findall(r"\([0-9,]+\)", buttons))
        joltage = tuple(int(a) for a in  joltage.split(","))
        out.append((lights, buttons, joltage))
    return out


def part1(data: Any) -> Any:
    """Solve part 1."""
    # Recompute for modulo math
    machines = []
    for lights, bts,_ in data:
        mod = 2**len(lights)
        lights = sum(l*(2**n) for n, l in enumerate(lights))
        bts = [sum(2**n for n in b) for b in bts]
        machines.append((mod, lights, bts))

    def neighbor(mod, bts):
        def _neigh(lights):
            for btn in bts:
                yield (lights^btn) % mod
        return _neigh

    def fewest_presses(mod, lights, bts):
        return bfs_one(
            start=0,
            neighbors=neighbor(mod, bts),
            is_goal=lambda x: x == lights
        ).goal_cost()

    return sum(fewest_presses(m,l,b) for m,l,b in machines) 


def part2(data: Any) -> Any:
    """Solve part 2."""

    def fewest_presses(buttons, joltages):

        # For each joltage dial, find the buttons that can manipulate it
        j_bts = [[] for i, _ in enumerate(joltages)]

        for i, btn in enumerate(buttons):
            for dial in btn:
               j_bts[dial].append(i)

        # Now, we know that number of btn presses must equal the dial settings
        #
        # E.g. for a btn like this a->d and dial x,y,z,q
        # x = a + b
        # y = b + c + d
        # z = a + d
        # q = b + d
        #
        # We solve for
        # min(sum(a, b, c, d))

        # We use Z3
        # Define vars using Int(x_i), one for each button
        vars = [Int(f"x{i}") for i, _ in enumerate(buttons)]

        # Initialize the solver
        solver = Optimize()

        # Add assumptions (x_i >= 0)
        solver.add([v >= 0 for v in vars])

        # Add an equation for each dial D (D_j == x_j0 ... x_jn)
        for j, dial_setting in enumerate(joltages):
            solver.add(Sum([vars[i] for i in j_bts[j]]) == dial_setting)

        # Find the solution that minimizes the sum of vars
        solver.minimize(Sum(vars))

        if solver.check() != sat:
            raise RuntimeError("No solution found")
        
        model = solver.model()

        # print([m.evaluate(v).as_long() for v in xs]) # Print button presses
        return int(model.evaluate(Sum(vars)).as_long())

    return sum(fewest_presses(b,j) for n, (_,b,j) in prog(data))


def main() -> None:
    raw = read_input(DAY)
    data = parse_input(raw)

    p1 = time_call(part1, data)
    print(f"Year {AOC_YEAR} Day {DAY} - Part 1: {p1.value} ({p1.seconds:.3f}s)")

    raw = read_input(DAY)
    data = parse_input(raw)

    p2 = time_call(part2, data)
    print(f"Year {AOC_YEAR} Day {DAY} - Part 2: {p2.value} ({p2.seconds:.3f}s)")


if __name__ == "__main__":
    main()
