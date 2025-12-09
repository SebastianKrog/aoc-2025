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
#from aoc.search import bfs, bfs_one, dfs, astar, build_graph
#from aoc.iteration import split_by, unique_permutations, nwise

from aoc.common import read_input, time_call
from aoc.config import AOC_YEAR

DAY = {day}


def parse_input(raw: str) -> Any:
    """Convert the raw text into a convenient structure."""
    return raw.rstrip("\n").splitlines()


def part1(data: Any) -> Any:
    """Solve part 1."""

    return data


def part2(data: Any) -> Any:
    """Solve part 2."""

    return data


def main() -> None:
    raw = read_input(DAY)
    data = parse_input(raw)

    p1 = time_call(part1, data)
    print(f"Year {{AOC_YEAR}} Day {{DAY}} - Part 1: {{p1.value}} ({{p1.seconds:.3f}}s)")

    raw = read_input(DAY)
    data = parse_input(raw)

    #p2 = time_call(part2, data)
    #print(f"Year {{AOC_YEAR}} Day {{DAY}} - Part 2: {{p2.value}} ({{p2.seconds:.3f}}s)")


if __name__ == "__main__":
    main()
