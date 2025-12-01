from __future__ import annotations

import argparse
import importlib
import subprocess
from pathlib import Path

from .client import save_day_data
from .config import ROOT, AOC_YEAR
from .common import day_dir

# Templates from section 5:
# DAY_TEMPLATE
# TEST_TEMPLATE

DAY_TEMPLATE = """\
from __future__ import annotations

from typing import Any

#import re
#from itertools import combinations, permutations, product
#from math import prod, lcm

#from aoc.progress import prog # Add a progress bar when needed (used as enumerate)

#from aoc.grid import NORTH, SOUTH, EAST, WEST, DIR4, neighbors4, parse_char_grid,
#  parse_int_grid, add_pos, UP, DOWN, LEFT, RIGHT, in_bounds
#from aoc.grid import NORTH, SOUTH, EAST, WEST, DIR8, neighbors8, parse_char_grid,
#  NORTH_EAST as NE, NORTH_WEST as NW, SOUTH_EAST as SE, SOUTH_WEST as SW
#from aoc.search import bfs, bfs_one, dfs, astar, build_graph
#from aoc.iteration import split_by, unique_permutations

from aoc.common import read_input, time_call
from aoc.config import AOC_YEAR

DAY = {day}


def parse_input(raw: str) -> Any:
    \"\"\"Convert the raw text into a convenient structure.\"\"\"
    return raw.rstrip("\\n").splitlines()


def part1(data: Any) -> Any:
    \"\"\"Solve part 1.\"\"\"

    return data


def part2(data: Any) -> Any:
    \"\"\"Solve part 2.\"\"\"

    return data


def main() -> None:
    raw = read_input(DAY)
    data = parse_input(raw)

    p1 = time_call(part1, data)
    print(f"Year {{AOC_YEAR}} Day {{DAY}} - Part 1: {{p1.value}} ({{p1.seconds:.3f}}s)")

    raw = read_input(DAY)
    data = parse_input(raw)

    #p2 = time_call(part2, data)
    #print(f"Year {{AOC_YEAR}} Day {{DAY}} - Part 2: {{p2.value}} ({{p2.seconds:.3f}}s)")


if __name__ == "__main__":
    main()
"""


TEST_TEMPLATE = """\
from __future__ import annotations
import pytest

from aoc.common import read_example

DAY = {day}


def test_example_part1():
    raw = read_example(DAY, idx=1)
    from days.day{day:02d} import parse_input, part1

    data = parse_input(raw)
    # Replace 0 with the expected answer for part 1.
    assert part1(data) == 0

@pytest.mark.skip(reason="Skip until you've done part1")
def test_example_part2():
    raw = read_example(DAY, idx=1)
    from days.day{day:02d} import parse_input, part2

    data = parse_input(raw)
    # Replace 0 with the expected answer for part 2.
    assert part2(data) == 0
"""


def _ensure_days_package() -> Path:
    days_pkg = ROOT / "days"
    days_pkg.mkdir(parents=True, exist_ok=True)
    init_file = days_pkg / "__init__.py"
    if not init_file.exists():
        init_file.write_text("", encoding="utf-8")
    return days_pkg


def _ensure_tests_dir() -> Path:
    tests_dir = ROOT / "tests"
    tests_dir.mkdir(parents=True, exist_ok=True)
    init_file = tests_dir / "__init__.py"
    if not init_file.exists():
        init_file.write_text("", encoding="utf-8")
    return tests_dir


def cmd_init_day(args: argparse.Namespace) -> None:
    day = args.day
    overwrite = args.overwrite

    result = save_day_data(day, overwrite=overwrite)

    days_pkg = _ensure_days_package()
    day_mod_path = days_pkg / f"day{day:02d}.py"
    # IMPORTANT: we never overwrite your solution code here
    if not day_mod_path.exists():
        day_mod_path.write_text(
            DAY_TEMPLATE.format(day=day),
            encoding="utf-8",
        )

    tests_dir = _ensure_tests_dir()
    test_file = tests_dir / f"test_day{day:02d}.py"
    # Likewise, don't overwrite tests you may have edited
    if not test_file.exists():
        test_file.write_text(
            TEST_TEMPLATE.format(day=day),
            encoding="utf-8",
        )

    print(f"Initialised year={result.year} day={day:02d}")
    print(f"  Input:    {result.input_path}")
    if result.example_paths:
        print("  Examples:")
        for p in result.example_paths:
            print(f"    - {p}")
    else:
        print("  Examples: (no <pre> blocks found)")

    if result.question_text_path:
        print(f"  Question text (md): {result.question_text_path}")
    if result.question_html_path:
        print(f"  Question HTML:      {result.question_html_path}")

    print(f"  Solution template:  {day_mod_path}")
    print(f"  Test template:      {test_file}")


def cmd_run(args: argparse.Namespace) -> None:
    day = args.day
    module_name = f"days.day{day:02d}"

    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError as exc:
        raise SystemExit(f"Could not import {module_name}: {exc}")

    if not hasattr(module, "main"):
        raise SystemExit(f"Module {module_name} has no main() function.")

    module.main()  # type: ignore[call-arg]


def cmd_test(args: argparse.Namespace) -> None:
    day = args.day
    tests_dir = ROOT / "tests"
    test_path = tests_dir / f"test_day{day:02d}.py"
    if not test_path.exists():
        raise SystemExit(f"No test file at {test_path}")

    cmd = ["pytest", "-q", str(test_path)]
    result = subprocess.run(cmd)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="aoc",
        description=f"Advent of Code helper CLI (Python, year {AOC_YEAR}).",
    )
    sub = p.add_subparsers(dest="command", required=True)

    sp_init = sub.add_parser(
        "init-day",
        help="Fetch input/examples/question and scaffold code + tests for a given day.",
    )
    sp_init.add_argument("day", type=int, help="AoC day (1-25)")
    sp_init.add_argument(
        "--overwrite",
        action="store_true",
        help=(
            "Overwrite input/examples/question files. "
            "Solution and test files are never overwritten."
        ),
    )
    sp_init.set_defaults(func=cmd_init_day)

    sp_run = sub.add_parser(
        "run",
        help="Run the solution module's main() for a given day.",
    )
    sp_run.add_argument("day", type=int, help="AoC day (1-25)")
    sp_run.set_defaults(func=cmd_run)

    sp_test = sub.add_parser(
        "test",
        help="Run pytest for a single day's tests.",
    )
    sp_test.add_argument("day", type=int, help="AoC day (1-25)")
    sp_test.set_defaults(func=cmd_test)

    return p


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    func = getattr(args, "func", None)
    if func is None:
        parser.print_help()
        return
    func(args)


if __name__ == "__main__":
    main()
