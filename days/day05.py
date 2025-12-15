from __future__ import annotations

from typing import Any

from re import findall

from aoc.iteration import split_by

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
    p1 = time_call(lambda x: part1(parse_input(x)), read_input(DAY))
    print(f"{AOC_YEAR} Day {DAY} - Part 1: {p1.value} ({p1.seconds:.3f}s)")

    p2 = time_call(lambda x: part2(parse_input(x)), read_input(DAY))
    print(f"{AOC_YEAR} Day {DAY} - Part 2: {p2.value} ({p2.seconds:.3f}s)")


if __name__ == "__main__":
    main()
