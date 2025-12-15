from __future__ import annotations
import pytest
from aoc.common import read_example
from days.day10 import parse_input, part1, part2

DAY = 10


def test_example_part1():
    raw = read_example(DAY, idx=1)
    assert part1(parse_input(raw)) == 7


def test_example_part2():
    raw = read_example(DAY, idx=1)
    assert part2(parse_input(raw)) == 33


def test_example_part2_2():
    raw = read_example(DAY, idx=6)
    assert part2(parse_input(raw)) == 316
