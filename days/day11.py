from __future__ import annotations

from typing import Any

from aoc.search import build_graph, count_paths

from aoc.common import read_input, time_call
from aoc.config import AOC_YEAR

DAY = 11


def parse_input(raw: str) -> Any:
    """Convert the raw text into a convenient structure."""
    input = raw.rstrip("\n").splitlines()
    return build_graph(input, lambda x: (x[:3], x[5:].split(" ")))


def part1(data: Any) -> Any:
    """Solve part 1."""

    def neighbors(n): return data.get(n)

    return count_paths("you", neighbors, "out")


def part2(data: Any) -> Any:
    """Solve part 2."""
    
    def neighbors(n):
        node, dac, fft = n
        if node not in data: return []
        for nxt in data.get(node):
            if nxt == "dac": yield nxt, True, fft
            elif nxt == "fft": yield nxt, dac, True
            else: yield nxt, dac, fft

    return count_paths(
        start = ("svr", False, False),
        neighbors=neighbors,
        goal = ("out", True, True)
    )


def main() -> None:
    p1 = time_call(lambda x: part1(parse_input(x)), read_input(DAY))
    print(f"{AOC_YEAR} Day {DAY} - Part 1: {p1.value} ({p1.seconds:.3f}s)")

    p2 = time_call(lambda x: part2(parse_input(x)), read_input(DAY))
    print(f"{AOC_YEAR} Day {DAY} - Part 2: {p2.value} ({p2.seconds:.3f}s)")


if __name__ == "__main__":
    main()
