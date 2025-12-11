from __future__ import annotations

from typing import Any

#import re
#from itertools import combinations, permutations, product
#from math import prod, lcm, ceil, floor, gcd

#from aoc.progress import prog # Add a progress bar when needed (used as enumerate)

#from aoc.grid import NORTH, SOUTH, EAST, WEST, DIR4, neighbors4, parse_char_grid,
#  parse_int_grid, add_pos, UP, DOWN, LEFT, RIGHT, in_bounds
#from aoc.grid import NORTH, SOUTH, EAST, WEST, DIR8, neighbors8, parse_char_grid,
#  NORTH_EAST as NE, NORTH_WEST as NW, SOUTH_EAST as SE, SOUTH_WEST as SW
from aoc.search import build_graph, count_paths #bfs, bfs_one, dfs, astar, 
#from aoc.iteration import split_by, unique_permutations, nwise

from aoc.common import read_input, time_call
from aoc.config import AOC_YEAR

DAY = 11


def parse_input(raw: str) -> Any:
    """Convert the raw text into a convenient structure."""
    input = raw.rstrip("\n").splitlines()
    return build_graph(input, lambda x: (x[:3], x[5:].split(" ")))


def part1(data: Any) -> Any:
    """Solve part 1."""

    def neighbors(n): return data.get(n)

    return count_paths("you", neighbors, "out")


def part2(data: Any) -> Any:
    """Solve part 2."""
    
    def neighbors(n):
        node, dac, fft = n
        if node not in data: return []
        for nxt in data.get(node):
            if nxt == "dac": yield nxt, True, fft
            elif nxt == "fft": yield nxt, dac, True
            else: yield nxt, dac, fft

    return count_paths(
        start = ("svr", False, False),
        neighbors=neighbors,
        goal = ("out", True, True)
    )


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
