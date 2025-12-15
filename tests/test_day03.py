from __future__ import annotations
import pytest

from aoc.common import read_example

DAY = 3


def test_example_part1():
    raw = read_example(DAY, idx=1)
    from days.day03 import parse_input, part1

    assert part1(parse_input(raw)) == 357


def test_example_part2():
    raw = read_example(DAY, idx=1)
    from days.day03 import parse_input, part2

    assert part2(parse_input(raw)) == 3121910778619
