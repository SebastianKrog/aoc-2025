from __future__ import annotations
import pytest
from aoc.common import read_example
from days.day12 import parse_input, part1

DAY = 12


def test_example_part1():
    raw = read_example(DAY, idx=6)
    assert part1(parse_input(raw)) == 0
