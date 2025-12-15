from __future__ import annotations

from typing import Any

from itertools import combinations
from math import prod

from aoc.common import read_input, time_call
from aoc.config import AOC_YEAR

DAY = 8


def parse_input(raw: str) -> Any:
    """Convert the raw text into a convenient structure."""
    input = raw.rstrip("\n").splitlines()
    return [tuple(int(a) for a in l.split(",")) for l in input]


def sort_by_dist(points):
    def dist_ish(p1, p2):
        (x1,y1,z1), (x2,y2,z2) = p1, p2
        return (x2-x1)**2+(y2-y1)**2+(z2-z1)**2
    
    dists = [(p1, p2, dist_ish(p1,p2)) for p1, p2 in combinations(points,2)]
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
        if max_n is None and len(seen) == n_points and len(networks) == 1:
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
    p1 = time_call(lambda x: part1(parse_input(x)), read_input(DAY))
    print(f"{AOC_YEAR} Day {DAY} - Part 1: {p1.value} ({p1.seconds:.3f}s)")

    p2 = time_call(lambda x: part2(parse_input(x)), read_input(DAY))
    print(f"{AOC_YEAR} Day {DAY} - Part 2: {p2.value} ({p2.seconds:.3f}s)")


if __name__ == "__main__":
    main()
