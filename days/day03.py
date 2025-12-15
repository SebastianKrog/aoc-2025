from __future__ import annotations

from typing import Any

from re import findall

from aoc.common import read_input, time_call
from aoc.config import AOC_YEAR

DAY = 3


def parse_input(raw: str) -> Any:
    """Convert the raw text into a convenient structure."""
    input = raw.rstrip("\n").splitlines()
    return [findall(r"(\d)", l) for l in input]


def part1(data: Any) -> Any:
    """Solve part 1."""

    def max_joltage(l):
        for n in range(99,10,-1):
            n1, n2 = list(str(n))
            if n1 == n2:
                if l.count(n1) > 1:
                    return n
            elif n1 in l:
                n1i = l.index(n1)
                if n2 in l[n1i:]:
                    return n

    return sum(max_joltage(l) for l in data)


def part2(data: Any) -> Any:
    """Solve part 2."""

    def joltage(l, found):
        if len(found) == 12: return int("".join(found))
        sublist = l[:len(l)-(11-len(found))]
        for i in range(9, 0, -1):
            if str(i) in sublist: break
        idx = sublist.index(str(i))
        return joltage(l[idx+1:], found+[l[idx]])

    return sum(joltage(l, []) for l in data)


def main() -> None:
    p1 = time_call(lambda x: part1(parse_input(x)), read_input(DAY))
    print(f"{AOC_YEAR} Day {DAY} - Part 1: {p1.value} ({p1.seconds:.3f}s)")

    p2 = time_call(lambda x: part2(parse_input(x)), read_input(DAY))
    print(f"{AOC_YEAR} Day {DAY} - Part 2: {p2.value} ({p2.seconds:.3f}s)")


if __name__ == "__main__":
    main()
