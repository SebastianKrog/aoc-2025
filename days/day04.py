from __future__ import annotations

from typing import Any

#import re
#from itertools import combinations, permutations, product
#from math import prod, lcm, ceil, floor, gcd

#from aoc.progress import prog # Add a progress bar when needed (used as enumerate)

#from aoc.grid import NORTH, SOUTH, EAST, WEST, DIR4, neighbors4, parse_char_grid,
#  parse_int_grid, add_pos, UP, DOWN, LEFT, RIGHT, in_bounds
from aoc.grid import neighbors8, parse_char_grid, iter_grid
#from aoc.search import bfs, bfs_one, dfs, astar, build_graph
#from aoc.iteration import split_by, unique_permutations

from aoc.common import read_input, time_call
from aoc.config import AOC_YEAR

DAY = 4


def parse_input(raw: str) -> Any:
    """Convert the raw text into a convenient structure."""
    return parse_char_grid(raw)


def part1(data: Any) -> Any:
    """Solve part 1."""
    zum = 0
    for pos, var in iter_grid(data):
        if var != "@": continue
        if sum(data[r][c] == "@" for r,c
               in neighbors8(pos, data)) < 4:
            zum += 1

    return zum


def part2(data: Any) -> Any:
    """Solve part 2."""

    rolls = set(p for p, v in iter_grid(data) if v == "@")

    zum = None
    nzum = 0
    while nzum != zum:
        zum = nzum
        for pos in list(rolls):
            if sum(pos in rolls for pos 
                   in neighbors8(pos, data)) < 4:
                rolls.remove(pos)
                nzum += 1
    return zum


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
