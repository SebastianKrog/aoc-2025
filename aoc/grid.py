from __future__ import annotations

import sys
from typing import Any, Callable, Iterable, Iterator, Mapping, Sequence, TypeVar

T = TypeVar("T")
Pos = tuple[int, int]

# Coordinate convention: (row, col)
# row increases downward, col increases to the right.

NORTH: Pos = (-1, 0)
SOUTH: Pos = (1, 0)
WEST: Pos = (0, -1)
EAST: Pos = (0, 1)

UP: Pos = NORTH
DOWN: Pos = SOUTH
LEFT: Pos = WEST
RIGHT: Pos = EAST

NORTH_EAST: Pos = (-1, 1)
NORTH_WEST: Pos = (-1, -1)
SOUTH_EAST: Pos = (1, 1)
SOUTH_WEST: Pos = (1, -1)

DIR4: tuple[Pos, ...] = (NORTH, SOUTH, WEST, EAST)
DIR_CARDINAL: tuple[Pos, ...] = DIR4
DIR_DIAGONAL: tuple[Pos, ...] = (NORTH_EAST, NORTH_WEST, SOUTH_EAST, SOUTH_WEST)
DIR8: tuple[Pos, ...] = DIR4 + DIR_DIAGONAL


def add_pos(a: Pos, b: Pos) -> Pos:
    """Add two (row, col) positions or deltas."""
    return a[0] + b[0], a[1] + b[1]


def delta_pos(a: Pos, b: Pos) -> Pos:
    """Return the delta a - b (component-wise)."""
    return a[0] - b[0], a[1] - b[1]


def parse_char_grid(
    raw: str,
    *,
    trim: bool = True,
    keep_empty: bool = False,
) -> list[list[str]]:
    """Parse a multiline string into a list-of-lists of characters."""
    lines = raw.splitlines()
    if trim:
        lines = [line.rstrip("\n") for line in lines]
    if not keep_empty:
        lines = [line for line in lines if line]
    return [list(line) for line in lines]


def parse_int_grid(
    raw: str,
    *,
    trim: bool = True,
    keep_empty: bool = False,
    base: int = 10,
) -> list[list[int]]:
    """Parse a multiline string of digits into a grid of ints."""
    char_grid = parse_char_grid(raw, trim=trim, keep_empty=keep_empty)
    return [[int(ch, base) for ch in row] for row in char_grid]


def add_border(
    grid: Sequence[Sequence[T]],
    border: T = ".",
    border_width: int = 1
) -> list[list[T]]:
    """Return a new grid with a n-cell border added around it."""
    if border_width < 0: raise ValueError("border_width must be >= 0")
    if not grid: return []

    bordered_width = max(len(row) for row in grid) + 2 * border_width

    border_row = [border] * bordered_width
    bordered = [border_row for _ in range(border_width)]
    for row in grid:
        bordered.append([border]*border_width + row + [border]*border_width)
    bordered.extend(border_row for _ in range(border_width))

    return bordered


def iter_grid(
    grid: Sequence[Sequence[T]],
) -> Iterator[tuple[Pos, T]]:
    """Yield ((row, col), value) for every cell in row-major order."""
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            yield (r, c), val


def in_bounds(pos: Pos, grid: Sequence[Sequence[T]]) -> bool:
    """Return True if pos is inside the grid bounds."""
    r, c = pos
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])


def find_first(needle: Any, grid: Sequence[Sequence[T]]) -> Pos | None:
    """Return the first position containing needle, or None if not found."""
    for (r, c), value in iter_grid(grid):
        if value == needle:
            return (r, c)
    return None


def neighbors4(
    pos: Pos,
    grid: Sequence[Sequence[T]],
    *,
    passable: Callable[[Pos, T], bool] | None = None,
) -> Iterable[Pos]:
    """4-neighbour moves (N, S, W, E) inside grid bounds."""
    r, c = pos
    rows = len(grid)
    cols = len(grid[0])
    for dr, dc in DIR4:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            value = grid[nr][nc]
            if passable is None or passable((nr, nc), value):
                yield (nr, nc)


def neighbors8(
    pos: Pos,
    grid: Sequence[Sequence[T]],
    *,
    passable: Callable[[Pos, T], bool] | None = None,
) -> Iterable[Pos]:
    """8-neighbour moves (including diagonals)."""
    r, c = pos
    rows = len(grid)
    cols = len(grid[0])
    for dr, dc in DIR8:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            value = grid[nr][nc]
            if passable is None or passable((nr, nc), value):
                yield (nr, nc)


def positions_to_grid(
    positions: Iterable[Pos],
    *,
    fill: str = ".",
    mark: str = "X",
    margin: int = 0,
) -> list[list[str]]:
    """Turn a set/list of positions into a small character grid.

    - positions: iterable of (row, col)
    - fill: background character
    - mark: character used for each position
    - margin: padding of empty cells around the bounding box
    """
    pos_set = set(positions)
    if not pos_set:
        return []

    min_r = min(r for r, _ in pos_set) - margin
    max_r = max(r for r, _ in pos_set) + margin
    min_c = min(c for _, c in pos_set) - margin
    max_c = max(c for _, c in pos_set) + margin

    rows = max_r - min_r + 1
    cols = max_c - min_c + 1

    grid: list[list[str]] = [[fill for _ in range(cols)] for _ in range(rows)]

    for r, c in pos_set:
        gr = r - min_r
        gc = c - min_c
        if 0 <= gr < rows and 0 <= gc < cols:
            grid[gr][gc] = mark

    return grid


# ---------------------------------------------------------------------------
# Printing a grid
# ---------------------------------------------------------------------------

def format_grid(
    grid: Sequence[Sequence[T]],
    *,
    sep: str = "",
    cell_to_str: Callable[[T], str] = str,
) -> str:
    """Return a string representation of a 2D grid."""
    lines: list[str] = []
    for row in grid:
        lines.append(sep.join(cell_to_str(cell) for cell in row))
    return "\n".join(lines)


def grid_with_positions(
    grid: Sequence[Sequence[T]],
    positions: Iterable[Pos] | Mapping[Pos, T],
    *,
    default_mark: T,
    ignore_out_of_bounds: bool = True,
) -> list[list[T]]:
    """Return a copy of 'grid' with given positions overlaid.

    - positions can be:
        * an iterable of (row, col): all positions get 'default_mark'
        * a mapping {(row, col): value}: each position gets its own value
    """
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    result: list[list[T]] = [list(row) for row in grid]

    if isinstance(positions, Mapping):
        items = positions.items()
    else:
        items = ((pos, default_mark) for pos in positions)

    for (r, c), value in items:
        if 0 <= r < rows and 0 <= c < cols:
            mark_value = value if value is not None else default_mark
            result[r][c] = mark_value
        elif not ignore_out_of_bounds:
            raise IndexError(f"Position {(r, c)} is outside grid of size {rows}x{cols}")

    return result


def print_grid(
    grid: Sequence[Sequence[T]],
    *,
    sep: str = "",
    cell_to_str: Callable[[T], str] = str,
    positions: Iterable[Pos] | Mapping[Pos, T] | None = None,
    default_mark: T | None = None,
    ignore_out_of_bounds: bool = True,
    file=None,
) -> None:
    """Print a 2D grid, optionally overlaying positions.

    - positions:
        * None: just print the grid.
        * Iterable[(r, c)]: overlay all with default_mark.
        * Mapping[(r, c) -> value]: overlay each with its own value.
    - default_mark:
        * Required if positions is an iterable (non-mapping).
        * Used as fallback when mapping value is None.
    """
    if file is None:
        file = sys.stdout

    if positions is not None:
        if not isinstance(positions, Mapping) and default_mark is None:
            raise ValueError(
                "default_mark must be provided when positions is an iterable"
            )
        grid_to_print = grid_with_positions(
            grid,
            positions,
            default_mark=default_mark,  # type: ignore[arg-type]
            ignore_out_of_bounds=ignore_out_of_bounds,
        )
    else:
        grid_to_print = grid

    print(format_grid(grid_to_print, sep=sep, cell_to_str=cell_to_str), file=file)


def print_positions(
    positions: Iterable[Pos],
    *,
    fill: str = ".",
    mark: str = "X",
    margin: int = 0,
    sep: str = "",
    file=None,
) -> None:
    """Print only a set of positions as a small grid.

    Example:
        print_positions({(0, 0), (2, 3), (4, 1)}, mark="X", fill=".")
    """
    if file is None:
        file = sys.stdout

    grid = positions_to_grid(positions, fill=fill, mark=mark, margin=margin)
    if not grid:
        return

    print_grid(grid, sep=sep, file=file)
