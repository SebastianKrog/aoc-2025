from __future__ import annotations

from typing import Any

import re

from math import ceil

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
    p1 = time_call(lambda x: part1(parse_input(x)), read_input(DAY))
    print(f"{AOC_YEAR} Day {DAY} - Part 1: {p1.value} ({p1.seconds:.3f}s)")

    p2 = time_call(lambda x: part2(parse_input(x)), read_input(DAY))
    print(f"{AOC_YEAR} Day {DAY} - Part 2: {p2.value} ({p2.seconds:.3f}s)")

if __name__ == "__main__":
    main()
