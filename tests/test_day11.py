from __future__ import annotations
import pytest
from aoc.common import read_example
from days.day11 import parse_input, part1, part2

DAY = 11


def test_example_part1():
    raw = read_example(DAY, idx=1)
    assert part1(parse_input(raw)) == 5


def test_example_part2():
    raw = read_example(DAY, idx=2)
    assert part2(parse_input(raw)) == 2
