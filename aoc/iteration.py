from __future__ import annotations
from itertools import groupby
from collections.abc import Iterable as IterableABC, Callable as CallableABC
from collections import Counter
from typing import Iterable, Iterator, List, Tuple, TypeVar, Callable, Union

T = TypeVar("T")

# In many cases itertools combinations and permutations can do the job.
# Here is a collection of other tools that are sometimes useful.

def unique_permutations(
    iterable: Iterable[T],
    r: int | None = None,
) -> Iterator[Tuple[T, ...]]:
    """
    Yield unique permutations of `iterable`, even if it contains duplicates.

    Args:
        iterable: Input elements.
        r: Length of permutations. If None, use len(iterable).

    Yields:
        Tuples representing unique permutations.
    """
    items: List[T] = list(iterable)
    n = len(items)

    if r is None:
        r = n
    if r < 0 or r > n:
        # No permutations possible
        return

    counts: Counter[T] = Counter(items)
    perm: List[T] = []

    def backtrack() -> Iterator[Tuple[T, ...]]:
        if len(perm) == r:
            yield tuple(perm)
            return

        for x in counts:
            if counts[x] <= 0:
                continue
            counts[x] -= 1
            perm.append(x)
            yield from backtrack()
            perm.pop()
            counts[x] += 1

    yield from backtrack()


SepSpec = Union[
    Callable[[T], bool],  # predicate
    T,                    # single separator value
    Iterable[T],          # collection of separator values
]


def _make_predicate(sep_spec: SepSpec[T]) -> Callable[[T], bool]:
    """
    Normalize `sep_spec` to a predicate `p(x) -> True if x is a separator`.
    """
    if isinstance(sep_spec, CallableABC):
        return sep_spec

    if isinstance(sep_spec, (str, bytes)):
        value = sep_spec
        return lambda x, value=value: x == value

    if isinstance(sep_spec, IterableABC):
        try:
            seps = set(sep_spec)  # type: ignore[arg-type]
            return lambda x, seps=seps: x in seps
        except TypeError:
            seps_list = list(sep_spec)  # type: ignore[arg-type]
            return lambda x, seps_list=seps_list: x in seps_list

    if not hasattr(sep_spec, "__eq__"):
        raise TypeError(
            "is_separator must be a Callable, an Iterable, or a value "
            "that can be compared using '=='."
        )

    value = sep_spec
    return lambda x, value=value: x == value


def split_by(
    iterable: Iterable[T],
    is_separator: SepSpec[T],
    include_separator: bool = False,
) -> Iterator[List[T]]:
    """
    Split `iterable` into chunks using `is_separator` to mark separators.

    `is_separator` can be:
      - a predicate: Callable[[T], bool]
      - a single separator value: e.g. ""
      - an iterable of separator values: e.g. {"", None}

    If include_separator is False (default):
        separators are not included in the result.

    If include_separator is True:
        each run of one or more separator items becomes its own group.
    """
    pred = _make_predicate(is_separator)

    for is_sep, group in groupby(iterable, key=pred):
        chunk = list(group)
        if not chunk:
            continue
        if is_sep:
            if include_separator:
                yield chunk
        else:
            yield chunk
