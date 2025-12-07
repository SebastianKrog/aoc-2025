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
#from aoc.iteration import split_by, unique_permutations

from aoc.common import read_input, time_call
from aoc.config import AOC_YEAR

DAY = 7


def parse_input(raw: str) -> Any:
    """Convert the raw text into a convenient structure."""
    input = raw.rstrip("\n").splitlines()
    return (input[0].index("S"), 
            [set(n for n,i in enumerate(l) if i == "^") for l in input[1:]],
            len(input[0]))


def part1(data: Any) -> Any:
    """Solve part 1."""
    start, splitters, _ = data
    n_split = 0
    beams = set([start])

    for row in splitters:
        new_beams = set()
        for beam in beams:
            if beam in row:
                n_split += 1
                new_beams.add(beam-1)
                new_beams.add(beam+1)
            else: new_beams.add(beam)
        beams = new_beams

    return n_split


def part2(data: Any) -> Any:
    """Solve part 2."""

    start, splitters, width = data
    timelines = {i: 0 for i in range(width)}
    timelines[start] = 1

    for row in splitters:
        for tl, n in timelines.items():
            if n == 0: continue
            elif tl in row:
                timelines[tl] = 0
                timelines[tl+1] += n
                timelines[tl-1] += n

    return sum(timelines.values())


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
