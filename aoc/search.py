from __future__ import annotations

from collections import deque, defaultdict
from collections.abc import Callable, Hashable, Iterable
from dataclasses import dataclass
from functools import cache
from math import inf
from typing import DefaultDict, Generic, TypeAlias, TypeVar
import heapq

T = TypeVar("T", bound=Hashable)
U = TypeVar("U", bound=Hashable)
R = TypeVar("R")

Weight: TypeAlias = float | int


def reconstruct_path(parent: dict[T, T], end: T) -> list[T]:
    """Reconstruct a path from a root to 'end' using a parent map (stops when no parent exists)."""
    path: list[T] = [end]
    cur = end
    while cur in parent:
        cur = parent[cur]
        path.append(cur)
    path.reverse()
    return path


@dataclass
class SearchResult(Generic[T]):
    dist: dict[T, Weight]
    parent: dict[T, T]
    goal: T | None = None

    def path_to(self, target: T) -> list[T] | None:
        if target not in self.dist:
            return None
        return reconstruct_path(self.parent, target)

    def path_to_goal(self) -> list[T] | None:
        if self.goal is None or self.goal not in self.dist:
            return None
        return reconstruct_path(self.parent, self.goal)

    def cost_to(self, target: T) -> Weight | None:
        return self.dist.get(target)

    def goal_cost(self) -> Weight | None:
        if self.goal is None:
            return None
        return self.dist.get(self.goal)


def bfs(
    starts: Iterable[T],
    neighbors: Callable[[T], Iterable[T]],
    is_goal: Callable[[T], bool] | None = None,
) -> SearchResult[T]:
    """Breadth-first search from one or more start states (unweighted)."""
    dist: dict[T, int] = {}
    parent: dict[T, T] = {}
    q: deque[T] = deque()

    for s in starts:
        if s in dist:
            continue
        dist[s] = 0
        q.append(s)

    found: T | None = None

    while q:
        current = q.popleft()
        if is_goal is not None and is_goal(current):
            found = current
            break
        for nxt in neighbors(current):
            if nxt in dist:
                continue
            dist[nxt] = dist[current] + 1
            parent[nxt] = current
            q.append(nxt)

    return SearchResult(dist=dist, parent=parent, goal=found)


def bfs_one(
    start: T,
    neighbors: Callable[[T], Iterable[T]],
    is_goal: Callable[[T], bool] | None = None,
) -> SearchResult[T]:
    """Breadth-first search from one start states (unweighted)."""
    return bfs([start], neighbors, is_goal)


def dijkstra(
    starts: Iterable[T],
    neighbors: Callable[[T], Iterable[tuple[T, Weight]]],
    is_goal: Callable[[T], bool] | None = None,
) -> SearchResult[T]:
    """Dijkstra's algorithm for non-negative edge weights."""
    dist: dict[T, Weight] = {}
    parent: dict[T, T] = {}
    heap: list[tuple[Weight, T]] = []

    for s in starts:
        if s in dist:
            continue
        dist[s] = 0
        heapq.heappush(heap, (0, s))

    found: T | None = None

    while heap:
        d_cur, node = heapq.heappop(heap)
        if d_cur != dist.get(node, inf):
            continue

        if is_goal is not None and is_goal(node):
            found = node
            break

        for nxt, w in neighbors(node):
            new_d = d_cur + w
            if new_d < dist.get(nxt, inf):
                dist[nxt] = new_d
                parent[nxt] = node
                heapq.heappush(heap, (new_d, nxt))

    return SearchResult(dist=dist, parent=parent, goal=found)


def dijkstra_one(
    start: T,
    neighbors: Callable[[T], Iterable[tuple[T, Weight]]],
    is_goal: Callable[[T], bool] | None = None,
) -> SearchResult[T]:
    """Iterative depth-first traversal yielding nodes in pre-order."""
    return dijkstra([start], neighbors, is_goal)


def dfs(
    start: T,
    neighbors: Callable[[T], Iterable[T]],
    is_valid: Callable[[T], bool] | None = None,
) -> Iterable[T]:
    """Iterative depth-first traversal yielding nodes in pre-order."""
    seen: set[T] = set()
    stack: list[T] = [start]

    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)

        if is_valid is not None and not is_valid(node):
            continue

        yield node

        # Keep deterministic-ish order vs recursion by materializing and reversing.
        neigh_list = list(neighbors(node))
        for nxt in reversed(neigh_list):
            if nxt not in seen:
                stack.append(nxt)

    
def astar(
    starts: Iterable[T],
    is_goal: Callable[[T], bool],
    neighbors: Callable[[T], Iterable[tuple[T, Weight]]],
    heuristic: Callable[[T], float] | None = None,
) -> SearchResult[T]:
    """
    A* for non-negative edge weights.

    neighbors(state) -> iterable of (next_state, step_cost).
    heuristic(state) -> estimated remaining cost (>=0).
    """
    def _h(x: T) -> float:
        return 0.0 if heuristic is None else float(heuristic(x))

    open_heap: list[tuple[float, Weight, T]] = []
    parent: dict[T, T] = {}
    g: dict[T, Weight] = {}

    for s in starts:
        if s in g:
            continue
        g[s] = 0
        heapq.heappush(open_heap, (_h(s), 0, s))

    found: T | None = None

    while open_heap:
        _f, g_cur, node = heapq.heappop(open_heap)
        if g_cur != g.get(node, inf):
            continue

        if is_goal(node):
            found = node
            break

        for nxt, cost in neighbors(node):
            new_g = g_cur + cost
            if new_g < g.get(nxt, inf):
                g[nxt] = new_g
                parent[nxt] = node
                heapq.heappush(open_heap, (float(new_g) + _h(nxt), new_g, nxt))

    return SearchResult(dist=g, parent=parent, goal=found)


def astar_one(
    start: T,
    is_goal: Callable[[T], bool],
    neighbors: Callable[[T], Iterable[tuple[T, Weight]]],
    heuristic: Callable[[T], float] | None = None,
) -> SearchResult[T]:
    """
    A* for non-negative edge weights.

    neighbors(state) -> iterable of (next_state, step_cost).
    heuristic(state) -> estimated remaining cost (>=0).
    """
    return astar([start], is_goal, neighbors, heuristic)



def build_graph(
    lines: Iterable[str],
    parse_line: Callable[[str], tuple[U, Iterable[U]]],
    *,
    bidirectional: bool = False,
    dedupe: bool = True,
) -> dict[U, list[U]]:
    """Build an adjacency list graph from text lines.

    parse_line(line) -> (node, iterable_of_neighbors)

    bidirectional=True will add reverse edges for each neighbor.
    dedupe=True will remove duplicate edges while preserving first-seen order.
    """
    graph: DefaultDict[U, list[U]] = defaultdict(list)
    seen: DefaultDict[U, set[U]] = defaultdict(set)

    def _add_edge(a: U, b: U) -> None:
        if not dedupe:
            graph[a].append(b)
            return
        if b in seen[a]:
            return
        seen[a].add(b)
        graph[a].append(b)

    for line in lines:
        text = line.strip()
        if not text:
            continue
        node, neighs = parse_line(text)

        _ = graph[node]  # ensure key exists even if it has no neighbors

        for n in neighs:
            _add_edge(node, n)
            if bidirectional:
                _ = graph[n]
                _add_edge(n, node)

    return dict(graph)


def reduce_paths(
    start: T,
    neighbors: Callable[[T], Iterable[T]],
    goal: T | None = None,
    *,
    is_goal: Callable[[T], bool] | None = None,
    is_valid: Callable[[T], bool] | None = None,
    reduce_fn: Callable[[Iterable[R]], R],
    goal_value: R | Callable[[T], R],
    invalid_value: R | Callable[[T], R],
    empty_value: R | Callable[[T], R],
) -> R:
    """Reduce path-values in a DAG from start to a goal.

    dp(node):
      - if invalid -> invalid_value(node)
      - if goal    -> goal_value(node)
      - else       -> reduce_fn(dp(child) for child in neighbors(node))
                      (or empty_value(node) if no children)

    Raises ValueError if a cycle is detected.
    """
    if is_goal is None and goal is None:
        raise ValueError("Must supply either goal or is_goal.")

    def _val(v: R | Callable[[T], R], node: T) -> R:
        return v(node) if callable(v) else v

    visiting: set[T] = set()

    @cache
    def dp(node: T) -> R:
        if is_valid is not None and not is_valid(node):
            return _val(invalid_value, node)

        if is_goal is not None:
            if is_goal(node):
                return _val(goal_value, node)
        else:
            if node == goal:
                return _val(goal_value, node)

        if node in visiting:
            raise ValueError("Cycle detected: reduce_paths requires a DAG.")

        visiting.add(node)
        try:
            vals = [dp(nxt) for nxt in neighbors(node)]
            if not vals:
                return _val(empty_value, node)
            return reduce_fn(vals)
        finally:
            visiting.remove(node)

    return dp(start)


def count_paths(
    start: T,
    neighbors: Callable[[T], Iterable[T]],
    goal: T | None = None,
    *,
    is_goal: Callable[[T], bool] | None = None,
    is_valid: Callable[[T], bool] | None = None,
) -> int:
    """Count paths in a DAG from start to a goal (by value or predicate)."""
    return reduce_paths(
        start,
        neighbors,
        goal,
        is_goal=is_goal,
        is_valid=is_valid,
        reduce_fn=sum,
        goal_value=1,
        invalid_value=0,
        empty_value=0,
    )
