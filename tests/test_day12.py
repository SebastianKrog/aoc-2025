from __future__ import annotations
import pytest

from aoc.common import read_example

DAY = 12


def test_example_part1():
    raw = read_example(DAY, idx=6)
    from days.day12 import parse_input, part1

    data = parse_input(raw)
    # Replace 0 with the expected answer for part 1.
    assert part1(data) == 0
