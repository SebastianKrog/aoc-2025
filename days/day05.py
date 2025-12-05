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
from aoc.iteration import split_by, unique_permutations

from aoc.common import read_input, time_call
from aoc.config import AOC_YEAR

DAY = 5


def parse_input(raw: str) -> Any:
    """Convert the raw text into a convenient structure."""
    ranges, numbers = split_by(raw.rstrip("\n").splitlines(), "")
    ranges = [range(int(a), int(b)+1) for a,b in [findall(r"(\d+)-(\d+)", l)[0] for l in ranges]]
    numbers = map(int, numbers)
    return ranges, numbers


def part1(data: Any) -> Any:
    """Solve part 1."""
    ranges, numbers = data

    fresh = 0
    for i in numbers:
        for range in ranges:
            if i in range: 
                fresh +=1
                break

    return fresh


def part2(data: Any) -> Any:
    """Solve part 2."""
    ranges, _ = data
    ranges = sorted(ranges, key = lambda r: r[0])

    def find_overlap(x, y):
        return len(range(max(x[0], y[0]), min(x[-1], y[-1])+1)) != 0

    def combine_ranges(x, y):  
        return range(min(x[0], y[0]), max(x[-1], y[-1])+1)
    
    new_ranges = []
    for r in ranges:
        build_ranges = []
        for new_r in new_ranges:
            if find_overlap(r, new_r):
                r = combine_ranges(r, new_r)
            else:
                build_ranges.append(new_r)
        build_ranges.append(r)
        new_ranges = build_ranges
    
    return sum(len(r) for r in new_ranges)


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
