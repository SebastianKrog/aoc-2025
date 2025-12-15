from __future__ import annotations

from typing import Any

from aoc.grid import neighbors8, parse_char_grid, iter_grid

from aoc.common import read_input, time_call
from aoc.config import AOC_YEAR

DAY = 4


def parse_input(raw: str) -> Any:
    """Convert the raw text into a convenient structure."""
    return parse_char_grid(raw)


def part1(data: Any) -> Any:
    """Solve part 1."""
    zum = 0
    for pos, var in iter_grid(data):
        if var != "@": continue
        if sum(data[r][c] == "@" for r,c
               in neighbors8(pos, data)) < 4:
            zum += 1

    return zum


def part2(data: Any) -> Any:
    """Solve part 2."""

    rolls = set(p for p, v in iter_grid(data) if v == "@")

    zum = None
    nzum = 0
    while nzum != zum:
        zum = nzum
        for pos in list(rolls):
            if sum(pos in rolls for pos 
                   in neighbors8(pos, data)) < 4:
                rolls.remove(pos)
                nzum += 1
    return zum


def main() -> None:
    p1 = time_call(lambda x: part1(parse_input(x)), read_input(DAY))
    print(f"{AOC_YEAR} Day {DAY} - Part 1: {p1.value} ({p1.seconds:.3f}s)")

    p2 = time_call(lambda x: part2(parse_input(x)), read_input(DAY))
    print(f"{AOC_YEAR} Day {DAY} - Part 2: {p2.value} ({p2.seconds:.3f}s)")


if __name__ == "__main__":
    main()
