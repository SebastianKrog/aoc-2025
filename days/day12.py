from __future__ import annotations

from typing import Any

from re import findall
#from itertools import combinations, permutations, product
#from math import prod, lcm, ceil, floor, gcd

#from aoc.progress import prog # Add a progress bar when needed (used as enumerate)

from aoc.grid import iter_grid #, NORTH, SOUTH, EAST, WEST, DIR4, neighbors4,
#  parse_int_grid, add_pos, UP, DOWN, LEFT, RIGHT, in_bounds
#from aoc.grid import NORTH, SOUTH, EAST, WEST, DIR8, neighbors8, parse_char_grid,
#  NORTH_EAST as NE, NORTH_WEST as NW, SOUTH_EAST as SE, SOUTH_WEST as SW
#from aoc.search import bfs, bfs_one, dfs, astar, build_graph
from aoc.iteration import split_by#, unique_permutations, nwise

from aoc.common import read_input, time_call
from aoc.config import AOC_YEAR

DAY = 12


def parse_input(raw: str) -> Any:
    """Convert the raw text into a convenient structure."""
    input = raw.rstrip("\n").splitlines()
    figs = split_by(input[:6*5], "")
    figs = [tuple(f[1:4]) for f in figs]
    area_defs = [findall(r"(\d+)x(\d+): (\d+) (\d+) (\d+) (\d+) (\d+) (\d+)",l)[0] 
             for l in input[6*5:]]
    area_defs = [[int(i) for i in l] for l in area_defs]
    problems = [(tuple(l[0:2]), tuple(l[2:])) for l in area_defs]
    return figs, problems


def part1(data: Any) -> Any:
    """Solve part 1."""
    figs, problems = data
    
    # Calculate figure base costs.
    # These are best guesses for a repeating pattern of these symbols.
    sizes = tuple(sum(r.count("#") for r in f) for f in figs)
    costs = [c+f for c,f in zip(sizes, (2, 1, 1, 1, 1, 1))]

    # Calculate areas that are *definitely* unsovlable under somewhat generous assumptions
    solvable = []
    for area, counts in problems:
        area = area[0]*area[1]
        n = list(counts)

        # 0 2 2 2 2 0 fits neatly into a 6*9-4 area
        n_fit = min(n[1:5])//2
        n = n[:1]+[i-n_fit*2 for i in n[1:5]]+n[5:]
        area -= n_fit*(6*9-4)

        # 0 0 1 1 0 0 fits into a 3*4-1 area
        # We'll asume the -1 wont fit neatly
        n_fit = min(n[2:4])
        n = n[:2]+[i-n_fit for i in n[2:4]]+n[4:]
        area -= n_fit*(3*4)

        # Multiply by costs for the remaining
        cost = sum(n*c for n,c in zip(n, costs))
        area -= cost
        solvable.append(area)

    return sum(s >= 0 for s in solvable)


def part2(data: Any) -> Any:
    """Solve part 2."""

    return data


def main() -> None:
    raw = read_input(DAY)
    data = parse_input(raw)

    p1 = time_call(part1, data)
    print(f"Year {AOC_YEAR} Day {DAY} - Part 1: {p1.value} ({p1.seconds:.3f}s)")

    raw = read_input(DAY)
    data = parse_input(raw)

    #p2 = time_call(part2, data)
    #print(f"Year {AOC_YEAR} Day {DAY} - Part 2: {p2.value} ({p2.seconds:.3f}s)")


if __name__ == "__main__":
    main()
