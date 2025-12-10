from __future__ import annotations

from typing import Any

#import re
from itertools import combinations #, permutations, product
#from math import prod, lcm, ceil, floor, gcd

from aoc.progress import prog # Add a progress bar when needed (used as enumerate)

from aoc.grid import DIR4, add_pos, print_dict_grid #, NORTH, SOUTH, EAST, WEST, neighbors4, parse_char_grid,
#  parse_int_grid, add_pos, UP, DOWN, LEFT, RIGHT, in_bounds
#from aoc.grid import NORTH, SOUTH, EAST, WEST, DIR8, neighbors8, parse_char_grid,
#  NORTH_EAST as NE, NORTH_WEST as NW, SOUTH_EAST as SE, SOUTH_WEST as SW
from aoc.search import dfs #, astar, build_graph, bfs, bfs_one
from aoc.iteration import nwise #split_by, unique_permutations

from aoc.common import read_input, time_call
from aoc.config import AOC_YEAR

DAY = 9


def parse_input(raw: str) -> Any:
    """Convert the raw text into a convenient structure."""
    input = raw.rstrip("\n").splitlines()
    return [(int(a), int(b)) for a,b in [l.split(",") for l in input]]


def part1(data: Any) -> Any:
    """Solve part 1."""
    a_max = 0
    for (x1, y1), (x2, y2) in combinations(data, 2):
        area = (abs(x2-x1)+1)*(abs(y2-y1)+1)
        if area > a_max: a_max = area

    return a_max


def part2(data: Any) -> Any:
    """Solve part 2."""

    # Prepare edges
    r_edges = {}
    c_edges = {}
    for (r, c), (rn, cn) in nwise(data, circular=True):
        if r == rn:
            if r not in r_edges: r_edges[r] = []
            r_edges[r].append(range(min(c, cn), max(c, cn) + 1))
        if c == cn:
            if c not in c_edges: c_edges[c] = []
            c_edges[c].append(range(min(r, rn), max(r, rn) + 1))

    def eval_rect(p1, p2, a_max):
        if p1[0] == p2[0] or p1[1] == p2[1]: return a_max # ignore single width

        r1, c1 = min(p1[0], p2[0]), min(p1[1], p2[1]) 
        r2, c2 = max(p1[0], p2[0]), max(p1[1], p2[1])

        area = (r2-r1+1)*(c2-c1+1)
        if area <= a_max: return a_max

        for r in range(r1 + 1, r2):
            if r in r_edges:
                for ran in r_edges[r]:
                    if c1+1 in ran or c2-1 in ran: return a_max
        
        for c in range(c1 + 1, c2):
            if c in c_edges:
                for ran in c_edges[c]:
                    if r1+1 in ran or r2-1 in ran: return a_max

        return area

    a_max = 0
    total_comb = (len(data)*len(data)-1)//2
    for n, (p1, p2) in prog(combinations(data, 2), total=total_comb):
        a_max = eval_rect(p1, p2, a_max)
    
    return a_max


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
