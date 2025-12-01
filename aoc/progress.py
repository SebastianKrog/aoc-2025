from __future__ import annotations

import sys
import time
from typing import Iterable, Iterator, Tuple, TypeVar

T = TypeVar("T")


def prog(
    iterable: Iterable[T],
    *,
    total: int | None = None,
    prefix: str = "",
    bar_width: int = 30,
    min_runtime: float = 2.0,
    file = None,
) -> Iterator[Tuple[int, T]]:
    """
    Wrap an iterable and yield (index, item), printing a progress bar.

    - Works like enumerate(iterable), but shows progress.
    - Only shows a bar if the loop runs longer than min_runtime seconds.
    - If total is None, tries len(iterable); if that fails, uses an open-ended counter.

    Usage:
        for i, item in prog(data):
            ...

        for i, item in prog(data, prefix="Part 1 "):
            ...
    """
    if file is None:
        file = sys.stderr

    start = time.time()
    _total = total
    if _total is None:
        try:
            _total = len(iterable)  # type: ignore[arg-type]
        except TypeError:
            _total = None

    shown = False

    def show(idx: int) -> None:
        nonlocal shown
        now = time.time()
        # Only start showing after min_runtime
        if not shown and now - start < min_runtime:
            return
        shown = True

        if _total is not None:
            frac = min(1.0, (idx + 1) / _total)
            filled = int(frac * bar_width)
            bar = "#" * filled + "-" * (bar_width - filled)
            file.write(
                f"\r{prefix}[{bar}] {idx + 1}/{_total} ({frac*100:5.1f}%)"
            )
        else:
            file.write(f"\r{prefix}{idx + 1} items")
        file.flush()

    for idx, item in enumerate(iterable):
        show(idx)
        yield idx, item

    if shown:
        # Clear the line and move to a new one
        file.write("\r" + " " * (bar_width + 40) + "\r\n")
        file.flush()
