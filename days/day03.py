from __future__ import annotations

from typing import Any

from re import findall
#from itertools import combinations, permutations, product
#from math import prod, lcm, ceil, floor, gcd

#from aoc.progress import prog # Add a progress bar when needed (used as enumerate)

#from aoc.grid import NORTH, SOUTH, EAST, WEST, DIR4, neighbors4, parse_char_grid,
#  parse_int_grid, add_pos, UP, DOWN, LEFT, RIGHT, in_bounds
#from aoc.grid import NORTH, SOUTH, EAST, WEST, DIR8, neighbors8, parse_char_grid,
#  NORTH_EAST as NE, NORTH_WEST as NW, SOUTH_EAST as SE, SOUTH_WEST as SW
#from aoc.search import bfs, bfs_one, dfs, astar, build_graph
#from aoc.iteration import split_by, unique_permutations

from aoc.common import read_input, time_call
from aoc.config import AOC_YEAR

DAY = 3


def parse_input(raw: str) -> Any:
    """Convert the raw text into a convenient structure."""
    input = raw.rstrip("\n").splitlines()
    return [findall(r"(\d)", l) for l in input]


def part1(data: Any) -> Any:
    """Solve part 1."""

    def max_joltage(l):
        for n in range(99,10,-1):
            n1, n2 = list(str(n))
            if n1 == n2:
                if l.count(n1) > 1:
                    return n
            elif n1 in l:
                n1i = l.index(n1)
                if n2 in l[n1i:]:
                    return n

    return sum(max_joltage(l) for l in data)


def part2(data: Any) -> Any:
    """Solve part 2."""

    def joltage(l, found):
        if len(found) == 12: return int("".join(found))
        sublist = l[:len(l)-(11-len(found))]
        for i in range(9, 0, -1):
            i = str(i)
            if i in sublist:
                idx = sublist.index(i)
                break
        found.append(l[idx])
        return joltage(l[idx+1:], found)

    return sum(joltage(l, []) for l in data)


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
