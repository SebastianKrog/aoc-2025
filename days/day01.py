from __future__ import annotations

from typing import Any

import re

from aoc.common import read_input, time_call
from aoc.config import AOC_YEAR

DAY = 1


def parse_input(raw: str) -> Any:
    """Convert the raw text into a convenient structure."""
    return raw.rstrip("\n").splitlines()


def part1(data: Any) -> Any:
    """Solve part 1."""
    
    zeroes = 0
    dial = 50
    for line in data:
        dir, n = re.findall(r"(\D)(\d+)", line)[0]
        if dir == "L":
            n = -1 * int(n)
        else: n = int(n)
        dial += n
        dial %= 100
        if dial == 0: zeroes += 1

    return zeroes


def part2(data: Any) -> Any:
    """Solve part 2."""

    zeroes = 0
    dial = 50
    for line in data:
        dir, n = re.findall(r"(\D)(\d+)", line)[0]
        n = int(n)
        if dir == "L":
            for i in range(int(n)):
                dial -= 1
                if dial == 0: zeroes += 1
                if dial < 0: dial += 100
        else:
            for i in range(int(n)):
                dial += 1
                if dial > 99: dial -= 100
                if dial == 0: zeroes += 1

    return zeroes


def main() -> None:
    p1 = time_call(lambda x: part1(parse_input(x)), read_input(DAY))
    print(f"{AOC_YEAR} Day {DAY} - Part 1: {p1.value} ({p1.seconds:.3f}s)")

    p2 = time_call(lambda x: part2(parse_input(x)), read_input(DAY))
    print(f"{AOC_YEAR} Day {DAY} - Part 2: {p2.value} ({p2.seconds:.3f}s)")


if __name__ == "__main__":
    main()
