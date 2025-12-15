from __future__ import annotations
import pytest

from aoc.common import read_example

DAY = 6


def test_example_part1():
    raw = read_example(DAY, idx=1)
    from days.day06 import parse_input, part1

    assert part1(parse_input(raw)) == 4277556


def test_example_part2():
    raw = read_example(DAY, idx=1)
    from days.day06 import parse_input, part2

    assert part2(parse_input(raw)) == 3263827
