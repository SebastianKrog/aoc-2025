from __future__ import annotations

from typing import Any

from re import findall
#from itertools import combinations, permutations, product
#from math import prod, lcm, ceil, floor, gcd

from aoc.progress import prog # Add a progress bar when needed (used as enumerate)

#from aoc.grid import NORTH, SOUTH, EAST, WEST, DIR4, neighbors4, parse_char_grid,
#  parse_int_grid, add_pos, UP, DOWN, LEFT, RIGHT, in_bounds
#from aoc.grid import NORTH, SOUTH, EAST, WEST, DIR8, neighbors8, parse_char_grid,
#  NORTH_EAST as NE, NORTH_WEST as NW, SOUTH_EAST as SE, SOUTH_WEST as SW
from aoc.search import bfs_one #, dfs, astar, build_graph, bfs
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
        buttons = [(int(a) for a in l.strip("()").split(","))
                   for l in findall(r"\([0-9,]+\)", buttons)]
        joltage = [int(a) for a in  joltage.split(",")]
        out.append((lights, buttons, joltage))
    return out


def part1(data: Any) -> Any:
    """Solve part 1."""

    machines = []
    for lights, bts,_ in data:
        mod = 2**len(lights)
        lights = sum(int(l)*(2**n) for n, l in enumerate(lights))
        bts = [sum(2**n for n in b) for b in bts]
        machines.append((mod, lights, bts))
    
    #print(machines)

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
        )

    #zum = 0
    #for i, (m,l,b) in enumerate(machines):
    #    n = fewest_presses(m,l,b)
    #    print(i, m,l,b, n.goal_cost(), n.path_to_goal())
    #    zum += n.goal_cost()

    return sum(fewest_presses(m,l,b).goal_cost() for m,l,b in machines) 


def part2(data: Any) -> Any:
    """Solve part 2."""

    def fewest_presses(bts, joltages):
        # For each joltage dial, find the buttons that can manipulate it
        j_bts = {i: set() for i,_ in enumerate(joltages)}
        for i, dial in enumerate(joltages):
            for j, btn in enumerate(bts):
                if i in btn: pass

        # For each btn, find the max number of times it can be pressed
        bts_max = {}
        for i, btn in enumerate(bts):
            btn_max = 10**6
            for j, dial in enumerate(btn):
               j_bts[i].add(j)
               btn_max = min(joltages[dial], btn_max)
            bts_max[i] = btn_max

        # Now, we know that number of btn presses must equal the dial settings
        print(j_bts, bts_max)
    
    for _,b,j in data:
        print(list(b),list(j))
        fewest_presses(b,j)
                
    return None
    


    return data


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
