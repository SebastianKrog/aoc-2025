from __future__ import annotations

import argparse
import importlib
import subprocess
from pathlib import Path

from .client import save_day_data
from .config import ROOT, AOC_YEAR
from .common import day_dir


def _load_template(name: str) -> str:
    """Load a template from the templates directory."""
    template_path = Path(__file__).parent / "templates" / f"{name}.py"
    return template_path.read_text(encoding="utf-8")


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

    result = save_day_data(day, overwrite=True)

    days_pkg = _ensure_days_package()
    day_mod_path = days_pkg / f"day{day:02d}.py"
    # IMPORTANT: we never overwrite your solution code here
    if not day_mod_path.exists():
        day_mod_path.write_text(
            _load_template("day_template").format(day=day),
            encoding="utf-8",
        )

    tests_dir = _ensure_tests_dir()
    test_file = tests_dir / f"test_day{day:02d}.py"
    # Likewise, don't overwrite tests you may have edited
    if not test_file.exists():
        test_file.write_text(
            _load_template("test_template").format(day=day),
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
        "init",
        help="Fetch input/examples/question and scaffold code + tests for a given day.",
    )
    sp_init.add_argument("day", type=int, help="AoC day (1-25)")
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
