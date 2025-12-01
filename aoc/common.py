from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
from typing import Any

from .config import INPUTS_DIR


def day_dir(day: int) -> Path:
    return INPUTS_DIR / f"day{day:02d}"


def input_path(day: int) -> Path:
    return day_dir(day) / "input.txt"


def example_path(day: int, idx: int = 1) -> Path:
    return day_dir(day) / f"example{idx}.txt"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").rstrip("\n") + "\n"


def read_input(day: int) -> str:
    return read_text(input_path(day))


def read_example(day: int, idx: int = 1) -> str:
    return read_text(example_path(day, idx))


@dataclass
class TimingResult:
    value: Any
    seconds: float


def time_call(fn, *args: Any, **kwargs: Any) -> TimingResult:
    start = perf_counter()
    value = fn(*args, **kwargs)
    end = perf_counter()
    return TimingResult(value=value, seconds=end - start)
