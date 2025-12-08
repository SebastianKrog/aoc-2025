from __future__ import annotations

from typing import Any

#import re
from itertools import combinations
from math import prod, sqrt

#from aoc.progress import prog # Add a progress bar when needed (used as enumerate)

#from aoc.grid import NORTH, SOUTH, EAST, WEST, DIR4, neighbors4, parse_char_grid,
#  parse_int_grid, add_pos, UP, DOWN, LEFT, RIGHT, in_bounds
#from aoc.grid import NORTH, SOUTH, EAST, WEST, DIR8, neighbors8, parse_char_grid,
#  NORTH_EAST as NE, NORTH_WEST as NW, SOUTH_EAST as SE, SOUTH_WEST as SW
#from aoc.search import bfs, bfs_one, dfs, astar, build_graph
#from aoc.iteration import split_by, unique_permutations

from aoc.common import read_input, time_call
from aoc.config import AOC_YEAR

DAY = 8


def parse_input(raw: str) -> Any:
    """Convert the raw text into a convenient structure."""
    input = raw.rstrip("\n").splitlines()
    return [tuple(int(a) for a in l.split(",")) for l in input]


def sort_by_dist(points):
    def dist3d(p1, p2):
        (x1,y1,z1), (x2,y2,z2) = p1, p2
        return sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)
    
    dists = [(p1, p2, dist3d(p1,p2)) for p1, p2 in combinations(points,2)]
    return sorted(dists, key=lambda x: x[2])


def group_into_networks(dists, max_n = None, n_points=None):
    n = max_n or len(dists)
    seen = set()
    networks = []
    for p1,p2,_ in dists[:n]:
        if not (p1 in seen or p2 in seen):
            networks.append(set([p1, p2]))
        else:
            new_networks = []
            new_nw = set([p1, p2])
            for nw in networks:
                if p1 in nw or p2 in nw:
                    new_nw = new_nw.union(nw)
                else: new_networks.append(nw)
            new_networks.append(new_nw)
            networks = new_networks
        seen.add(p1)
        seen.add(p2)
        if max_n is None:
            if len(seen) == n_points and len(networks) == 1:
                return p1, p2  # For part 2, just return the joining points
    return networks


def part1(data: Any, n) -> Any:
    """Solve part 1."""
    dists = sort_by_dist(data)
    networks = group_into_networks(dists, max_n=n)

    return prod(sorted([len(a) for a in networks])[-3:])


def part2(data: Any) -> Any:
    """Solve part 2."""
    dists = sort_by_dist(data)
    (x1,_,_), (x2,_,_) = group_into_networks(dists, None, len(data))

    return x1*x2


def main() -> None:
    raw = read_input(DAY)
    data = parse_input(raw)

    p1 = time_call(part1, data, 1000)
    print(f"Year {AOC_YEAR} Day {DAY} - Part 1: {p1.value} ({p1.seconds:.3f}s)")

    raw = read_input(DAY)
    data = parse_input(raw)

    p2 = time_call(part2, data)
    print(f"Year {AOC_YEAR} Day {DAY} - Part 2: {p2.value} ({p2.seconds:.3f}s)")


if __name__ == "__main__":
    main()
