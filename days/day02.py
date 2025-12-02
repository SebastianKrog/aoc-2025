from __future__ import annotations

from typing import Any

import re
#from itertools import combinations, permutations, product
from math import ceil

#from aoc.progress import prog # Add a progress bar when needed (used as enumerate)

#from aoc.grid import NORTH, SOUTH, EAST, WEST, DIR4, neighbors4, parse_char_grid,
#  parse_int_grid, add_pos, UP, DOWN, LEFT, RIGHT, in_bounds
#from aoc.grid import NORTH, SOUTH, EAST, WEST, DIR8, neighbors8, parse_char_grid,
#  NORTH_EAST as NE, NORTH_WEST as NW, SOUTH_EAST as SE, SOUTH_WEST as SW
#from aoc.search import bfs, bfs_one, dfs, astar, build_graph
#from aoc.iteration import split_by, unique_permutations

from aoc.common import read_input, time_call
from aoc.config import AOC_YEAR

DAY = 2


def parse_input(raw: str) -> Any:
    """Convert the raw text into a convenient structure."""
    input = ",".join(raw.rstrip("\n").splitlines())
    ranges = input.split(",")
    split_ranges = [re.findall(r"(\d+)-(\d+)", r)[0] for r in ranges if r != ""]
    return [(int(a), int(b)) for a,b in split_ranges]


def part1(data: Any) -> Any:
    """Solve part 1."""

    def lsplit(i: int):
        s = str(i)
        l = int(len(s)/2)
        if len(s) % 2: return 10**l
        return int(s[0:l])
    
    def dbl(i: int):
        return int(str(i)+str(i))
    
    zum = 0
    for mi, ma in data:
        for n in range(lsplit(mi), lsplit(ma)+1):
            i = dbl(n)
            if i > ma: break
            if mi <= i <= ma: 
                zum += i

    return zum


def part2(data: Any) -> Any:
    """Solve part 2."""

    def find_repeats(mi, ma):
        def div(mi: int, ma: int, denom):
            s_mi, s_ma = str(mi), str(ma)
            n_digits = ceil(len(s_ma)/denom)
            while len(s_mi) < len(s_ma):
                s_mi = "0"+s_mi
            return int(s_mi[0:n_digits]), int(s_ma[0:n_digits])
    
        def mul(i: int, n: int):
            return int(str(i)*n)
    
        found = set()
        for denom in range(2, len(str(ma)) + 1):
            dmi, dma = div(mi, ma, denom)
            for n in range(dmi, dma + 1):
                i = mul(n, denom)
                if i > ma: break
                if mi <= i <= ma and i not in found: 
                    found.add(i)

        return sum(found)

    return sum(find_repeats(mi, ma) for mi, ma in data)


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
