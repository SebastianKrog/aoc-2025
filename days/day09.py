from __future__ import annotations

from typing import Any

#import re
from itertools import combinations#, permutations, product
#from math import prod, lcm, ceil, floor, gcd

from aoc.progress import prog # Add a progress bar when needed (used as enumerate)

from aoc.grid import DIR4, add_pos, print_dict_grid #, NORTH, SOUTH, EAST, WEST, neighbors4, parse_char_grid,
#  parse_int_grid, add_pos, UP, DOWN, LEFT, RIGHT, in_bounds
#from aoc.grid import NORTH, SOUTH, EAST, WEST, DIR8, neighbors8, parse_char_grid,
#  NORTH_EAST as NE, NORTH_WEST as NW, SOUTH_EAST as SE, SOUTH_WEST as SW
from aoc.search import dfs #, astar, build_graph, bfs, bfs_one
#from aoc.iteration import split_by, unique_permutations

from aoc.common import read_input, time_call
from aoc.config import AOC_YEAR

DAY = 9


def parse_input(raw: str) -> Any:
    """Convert the raw text into a convenient structure."""
    input = raw.rstrip("\n").splitlines()
    return [(int(a), int(b)) for a,b in [l.split(",") for l in input]]


def part1(data: Any) -> Any:
    """Solve part 1."""
    # Crude
    max = 0
    for (x1, y1), (x2, y2) in combinations(data, 2):
        area = (abs(x2-x1)+1)*(abs(y2-y1)+1)
        if area > max: max = area
    return max


def part2(data: Any) -> Any:
    """Solve part 2."""

    # Draw the path
    print("Step 1: Path")
    grid = {}
    r_min, r_max, c_min, c_max = (10**6, 0, 10**6, 0)
    for (r, c), (rn, cn) in zip(data, data[1:]+[list(data[0])]):
        delta_r, delta_c = abs(rn - r), abs(cn - c)
        if delta_r > 0 and rn > r:
            for i in range(delta_r): grid[(r+i, c)] = "#"
        elif delta_r > 0 and rn < r:
            for i in range(delta_r): grid[(r-i, c)] = "#"
        elif delta_c > 0 and cn > c:
            for i in range(delta_c): grid[(r, c+i)] = "#"
        else: # delta_c > 0 and cn < c
            for i in range(delta_c): grid[(r, c-i)] = "#"
        if r < r_min: r_min = r
        if r > r_max: r_max = r
        if c < c_min: c_min = c
        if c > c_max: c_max = c

    # Fill in the loop
    print("Step 2: Fill background")
    print(r_min, r_max, c_min, c_max)
    for n,r in prog(range(r_min, r_max+1)):
        for c in range(c_min, c_max+1):
            if (r,c) not in grid:
                grid[(r,c)] = "X"

    print("Step 3: Fill loop")
    start = (r_min -1, c_min -1)

    def neighbors(pos):
        for d in DIR4:
            r,c = n_pos = add_pos(pos, d)
            if r > r_max + 1 or r < r_min -1: continue
            if c > c_max + 1 or c < c_min -1: continue
            if n_pos in grid:
                if grid[n_pos] == "#": continue
                grid[n_pos] = "."
            yield n_pos

    list(dfs(start, neighbors))

    #print(list(outside))
    #print_dict_grid(grid)

    # Check all combinations, but we will do some smart filtering
    print("Step 4: Combinations")
    def new_max_if_valid(p1, p2, a_max):
        (x1, y1), (x2, y2) = p1, p2
        # Assume it's not a long thin line
        if x1 == x2 or y1 == y2: return a_max  

        # Ignore smaller solutions
        area = (abs(x2-x1)+1)*(abs(y2-y1)+1)
        if area <= a_max: return a_max

        # Check the corners and center first
        center = min(x1, x2) + abs(x2 - x1)//2, min(y1, y2) + abs(y2 - y1)//2
        check_points = ((x1, y1), (x2, y2), (x2, y1), (x2, y1), center) # corners and center
        for p in check_points:
            if grid[p] == ".": return a_max
        
        # Check the whole rectangle
        for r in range(min(x1, x2), max(x1, x2) + 1):
            for c in range(min(y1, y2), max(y1, y2) + 1):
                if grid[(r,c)] == ".": return a_max
        
        return area

    a_max = 0
    for n, (p1, p2) in prog(combinations(data, 2)):
        a_max = new_max_if_valid(p1, p2, a_max)
        
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
