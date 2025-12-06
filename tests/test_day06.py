from __future__ import annotations
import pytest

from aoc.common import read_example

DAY = 6


def test_example_part1():
    raw = read_example(DAY, idx=1)
    from days.day06 import parse_input, part1

    data = parse_input(raw)
    # Replace 0 with the expected answer for part 1.
    assert part1(data) == 4277556


def test_example_part2():
    raw = read_example(DAY, idx=1)
    from days.day06 import parse_input, part2

    data = parse_input(raw)
    # Replace 0 with the expected answer for part 2.
    assert part2(data) == 3263827
