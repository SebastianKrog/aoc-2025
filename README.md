# Advent of Code Python Template

This repository is a small, year-specific template for solving Advent of Code in Python.

It provides:

* A CLI to:

  * Fetch daily input.
  * Fetch and store the full puzzle text (part 1 and later part 2).
  * Extract example blocks from the puzzle page.
  * Scaffold a day’s solution module and test file.

* A shared toolbox:

  * Direction constants (`NORTH`, `SOUTH`, `LEFT`, `RIGHT`, etc.).
  * Grid parsing and neighbour helpers.
  * Generic BFS, DFS, and A* search.
  * A text-driven graph builder for node/tree diagrams.

The focus is on “mostly basic Python” with minimal, well-known dependencies.

---

## Repository layout

Typical structure (one repo per AoC year):

```text
aoc-2023/
  aoc/
    __init__.py
    config.py
    common.py
    grid.py
    search.py
    client.py
    cli.py
  days/
    __init__.py
    day01.py
    day02.py
    ...
  inputs/
    day01/
      input.txt
      example1.txt
      example2.txt
    day02/
      input.txt
      ...
  questions/
    day01.md
    day01.html
    day02.md
    day02.html
    ...
  tests/
    __init__.py
    test_day01.py
    test_day02.py
    ...
  requirements.txt
  .env.example
  README.md
```

Each repository is dedicated to a single year (e.g. 2023, 2025), configured via `AOC_YEAR`.

---

## Requirements

* Python 3.11+ (earlier may work, but this is the target).
* A browser session cookie for Advent of Code (the `session` cookie).

---

## Installation

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## Configuration (.env)

Copy the example env file and edit it:

```bash
cp .env.example .env
```

`.env.example`:

```bash
# Advent of Code year for this repo
AOC_YEAR=2023

# Advent of Code session cookie (from your browser; keep this secret)
AOC_SESSION=put_your_session_cookie_here

# Optional polite User-Agent (customise if you like)
# AOC_USER_AGENT=github.com/yourname/aoc-2023 (Advent of Code helper script)
```

Set `AOC_YEAR` to the appropriate year for this repository (e.g. `2025` for `aoc-2025`).

---

## CLI usage

The CLI is implemented in `aoc/cli.py` and exposed via:

```bash
python -m aoc.cli <command> [args...]
```

### 1. Initialise a day

Fetch input, puzzle HTML, examples, and scaffold code + tests:

```bash
python -m aoc.cli init-day 1
```

This will:

* Create `inputs/day01/input.txt` with your personal input.
* Create `inputs/day01/example*.txt` (each `<pre>` block from the puzzle page).
* Create or update:

  * `questions/day01.html` (raw HTML puzzle page).
  * `questions/day01.md` (Markdown conversion of the puzzle description).
* Create solution and test templates (if they don’t exist):

  * `days/day01.py`
  * `tests/test_day01.py`

`init-day` accepts:

```bash
python -m aoc.cli init-day DAY [--overwrite]
```

* `DAY`: integer 1–25.
* `--overwrite`:

  * Re-fetches input, examples, and question files.
  * Does **not** overwrite your solution or test code; it only overwrites:

    * `inputs/dayXX/input.txt`
    * `inputs/dayXX/example*.txt`
    * `questions/dayXX.md`
    * `questions/dayXX.html`

### 2. Updating the puzzle text when part 2 unlocks

After you submit a correct answer for part 1 and Advent of Code reveals part 2:

```bash
python -m aoc.cli init-day 1 --overwrite
```

This:

* Refetches the puzzle page.
* Regenerates `questions/day01.html`.
* Regenerates `questions/day01.md`, which now includes both part 1 and part 2 text.
* Keeps your `days/day01.py` and `tests/test_day01.py` unchanged.

### 3. Run your solution

Each day module (`days/dayXX.py`) defines a `main()` function. Run it via:

```bash
python -m aoc.cli run 1
```

This:

* Reads `inputs/day01/input.txt`.
* Calls `parse_input`, then `part1` and `part2`.
* Prints answers and timings.

### 4. Run tests for a day

Tests are written with `pytest` per-day. To run tests for day 1:

```bash
python -m aoc.cli test 1
```

This runs `pytest` on `tests/test_day01.py`.

---

## Question text and Markdown

The full puzzle description is saved under `questions/`:

* Raw HTML: `questions/dayXX.html`
* Markdown: `questions/dayXX.md`

## Shared utilities

The `aoc` package includes a few generic helpers aimed at common Advent of Code patterns.

### `aoc.common`

Core helpers (simplified overview):

* `read_input(day: int) -> str`
* `read_example(day: int, idx: int = 1) -> str`
* `time_call(fn, *args, **kwargs) -> TimingResult`

`TimingResult` has `value` and `seconds`.

---

## Grid utilities (`aoc.grid`)

`aoc/grid.py` provides:

* Direction constants as `(row, col)` deltas:

  ```python
  NORTH = (-1, 0)
  SOUTH = (1, 0)
  WEST  = (0, -1)
  EAST  = (0, 1)

  UP    = NORTH
  DOWN  = SOUTH
  LEFT  = WEST
  RIGHT = EAST

  NORTH_EAST = (-1, 1)
  NORTH_WEST = (-1, -1)
  SOUTH_EAST = (1, 1)
  SOUTH_WEST = (1, -1)

  DIR4  = (NORTH, SOUTH, WEST, EAST)
  DIR8  = DIR4 + (NORTH_EAST, NORTH_WEST, SOUTH_EAST, SOUTH_WEST)
  ```

* Basic helpers:

  ```python
  from aoc.grid import (
      Pos,
      parse_char_grid,
      parse_int_grid,
      neighbors4,
      neighbors8,
      add_pos,
      in_bounds,
  )
  ```

  * `Pos = tuple[int, int]` as `(row, col)`.
  * `parse_char_grid(raw: str) -> list[list[str]]`
  * `parse_int_grid(raw: str) -> list[list[int]]`
  * `neighbors4(pos, grid, passable=None)` – yields 4-neighbours inside bounds; `passable(pos, value)` optional filter.
  * `neighbors8(...)` – same with diagonals.
  * `add_pos(a, b)` – add two `(row, col)` tuples.
  * `in_bounds(pos, grid)` – boolean.

### Example: BFS on a grid

```python
from aoc.grid import parse_char_grid, neighbors4, Pos
from aoc.search import bfs_one

def shortest_path_len(raw: str, start: Pos, goal: Pos) -> int:
    grid = parse_char_grid(raw)

    nbrs = lambda p: neighbors4(
        p,
        grid,
        passable=lambda pos, ch: ch != "#",  # walls as '#'
    )

    result = bfs_one(start, nbrs, is_goal=lambda p: p == goal)
    if result.goal is None:
        raise ValueError("no path")
    return result.dist[result.goal]
```

---

## Search utilities (`aoc.search`)

`aoc/search.py` provides generic BFS, DFS, and A* that work over any hashable state.

### BFS

```python
from aoc.search import bfs, bfs_one

# bfs(starts, neighbors, is_goal=None)
# neighbors: state -> iterable[state]
# is_goal:   state -> bool (optional)

result = bfs_one(
    start_state,
    neighbors=lambda s: ...,
    is_goal=lambda s: ...,
)

# Use:
result.dist      # dict[state, distance]
result.parent    # dict[child, parent]
result.goal      # goal state (if found)
path = result.path_to(target_state)  # reconstructed path or None
```

BFS is ideal for unweighted shortest paths and flood-fills.

### DFS

```python
from aoc.search import dfs

for node in dfs(start_state, neighbors=lambda s: ...):
    ...
```

Iterative DFS, yielding nodes in pre-order.

### A* search

```python
from aoc.search import astar
from aoc.grid import parse_char_grid, neighbors4, Pos

def heuristic(goal: Pos):
    gr, gc = goal
    return lambda p: abs(p[0] - gr) + abs(p[1] - gc)  # Manhattan

def astar_path(raw: str, start: Pos, goal: Pos):
    grid = parse_char_grid(raw)

    def nbrs(p: Pos):
        for np in neighbors4(p, grid, passable=lambda pos, ch: ch != "#"):
            # cost 1 per step
            yield np, 1.0

    path, cost = astar(
        start,
        is_goal=lambda p: p == goal,
        neighbors=nbrs,
        heuristic=heuristic(goal),
    )
    return path, cost
```

Signature:

```python
path, cost = astar(
    start,
    is_goal:   Callable[[T], bool],
    neighbors: Callable[[T], Iterable[tuple[T, float]]],
    heuristic: Callable[[T], float] | None = None,
)
```

Returns `(path_list_or_None, total_cost)`.

### Graph builder for node diagrams / trees

`build_graph` makes adjacency lists from text input using a parsing lambda.

```python
from aoc.search import build_graph, bfs_one

lines = [
    "A -> B, C",
    "B -> D",
    "C -> D, E",
]

graph = build_graph(
    lines,
    parse_line=lambda line: (
        line.split("->")[0].strip(),
        [n.strip() for n in line.split("->")[1].split(",")],
    ),
    bidirectional=False,
)

start = "A"
goal = "E"

nbrs = lambda node: graph.get(node, [])
res = bfs_one(start, nbrs, is_goal=lambda n: n == goal)
path = res.path_to(goal)  # ['A', 'C', 'E']
```

Signature:

```python
graph = build_graph(
    lines: Iterable[str],
    parse_line: Callable[[str], tuple[Node, Iterable[Node]]],
    bidirectional: bool = False,
)
```

* `parse_line` converts each line of text to `(node, neighbours)`.
* If `bidirectional=True`, reverse edges are added automatically.

---

## Suggested workflow per day

1. At unlock time (or later), fetch the day:

   ```bash
   python -m aoc.cli init-day 1
   ```

2. Open:

   * `questions/day01.md` in your editor to read the puzzle.
   * `days/day01.py` to implement:

     * `parse_input`
     * `part1`
     * `part2`
   * `tests/test_day01.py` to:

     * Select the correct `example*.txt`.
     * Fill in known example answers.

3. Implement and test:

   ```bash
   python -m aoc.cli run 1
   python -m aoc.cli test 1
   ```

4. After you solve part 1 and part 2 appears on the site:

   ```bash
   python -m aoc.cli init-day 1 --overwrite
   ```

   This updates the stored puzzle text to include part 2, plus any additional examples.

---

## Notes

* Your `AOC_SESSION` value is a private authentication cookie. Keep `.env` out of version control.
* The helpers are intentionally lightweight and generic so they can be adapted quickly to different puzzle styles.
* For a new year, clone this repo as a starting point, change `AOC_YEAR` in `.env.example`.
