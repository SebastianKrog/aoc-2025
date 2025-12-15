from __future__ import annotations

from typing import Any

from re import findall

from aoc.common import read_input, time_call
from aoc.config import AOC_YEAR

DAY = 12


def parse_input(raw: str) -> Any:
    """Convert the raw text into a convenient structure."""
    input = raw.rstrip("\n").splitlines()
    area_defs = [findall(r"(\d+)x(\d+): (\d+) (\d+) (\d+) (\d+) (\d+) (\d+)",l)[0] 
             for l in input[6*5:]]
    area_defs = [[int(i) for i in l] for l in area_defs]
    problems = [(tuple(l[0:2]), tuple(l[2:])) for l in area_defs]
    return problems


def part1(data: Any) -> Any:
    """Solve part 1."""
    
    return sum(x*y >= 9*sum(c) for (x,y), c in data)



def main() -> None:
    p1 = time_call(lambda x: part1(parse_input(x)), read_input(DAY))
    print(f"{AOC_YEAR} Day {DAY} - Part 1: {p1.value} ({p1.seconds:.3f}s)")


if __name__ == "__main__":
    main()
