from __future__ import annotations

from collections import deque, defaultdict
from dataclasses import dataclass
from math import inf
from typing import (
    Callable,
    DefaultDict,
    Generic,
    Hashable,
    Iterable,
    TypeVar,
)
import heapq

T = TypeVar("T", bound=Hashable)
U = TypeVar("U", bound=Hashable)


def reconstruct_path(parent: dict[T, T], end: T) -> list[T]:
    """Reconstruct a path from any root to 'end' using a parent map."""
    path: list[T] = [end]
    cur = end
    while cur in parent:
        cur = parent[cur]
        path.append(cur)
    path.reverse()
    return path


@dataclass
class SearchResult(Generic[T]):
    dist: dict[T, float | int]
    parent: dict[T, T]
    goal: T | None = None

    def path_to(self, target: T) -> list[T] | None:
        if target not in self.dist:
            return None
        return reconstruct_path(self.parent, target)
    
    def path_to_goal(self) -> list[T] | None:
        if self.goal is None:
            return None
        return reconstruct_path(self.parent, self.goal)
    
    def cost_to(self, target: T) -> float | int | None:
        return self.dist.get(target)

    def goal_cost(self) -> float | int | None:
        if self.goal is None:
            return None
        return self.dist[self.goal]


def bfs(
    starts: Iterable[T],
    neighbors: Callable[[T], Iterable[T]],
    is_goal: Callable[[T], bool] | None = None,
) -> SearchResult[T]:
    """Breadth-first search from one or more start states.

    - neighbors(state) -> iterable of next states (lambda-friendly)
    - is_goal(state) -> bool (optional)
    """
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
    """Convenience wrapper for BFS with a single start state."""
    return bfs([start], neighbors, is_goal)


def dijkstra(
    starts: Iterable[T],
    neighbors: Callable[[T], Iterable[tuple[T, float]]],
    is_goal: Callable[[T], bool] | None = None,
) -> SearchResult[T]:
    """Dijkstra's algorithm for non-negative edge weights.

    - starts: one or more start nodes
    - neighbors(state) -> iterable of (next_state, step_cost)
    - is_goal(state) -> bool (optional early stop)
    """
    dist: dict[T, float] = {}
    parent: dict[T, T] = {}
    heap: list[tuple[float, T]] = []

    for s in starts:
        if s in dist:
            continue
        dist[s] = 0.0
        heapq.heappush(heap, (0.0, s))

    found: T | None = None

    while heap:
        d_cur, node = heapq.heappop(heap)
        if d_cur != dist.get(node, inf):
            # Stale heap entry
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
    neighbors: Callable[[T], Iterable[tuple[T, float]]],
    is_goal: Callable[[T], bool] | None = None,
) -> SearchResult[T]:
    """Convenience wrapper for Dijkstra with a single start state."""
    return dijkstra([start], neighbors, is_goal)


def dfs(
    start: T,
    neighbors: Callable[[T], Iterable[T]],
    is_valid: Callable[[T], bool] | None = None,
) -> Iterable[T]:
    """Iterative depth-first search, yielding nodes in pre-order.

    is_valid(node) -> bool (optional): if provided and returns False,
    the node is not yielded and its neighbors are not explored. The
    check is done once per node, after the seen-check.
    """
    seen: set[T] = set()
    stack: list[T] = [start]

    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)

        if is_valid is not None and not is_valid(node):
            # Skip yielding and do not expand neighbors
            continue

        yield node

        # Reverse to roughly preserve left-to-right order vs recursion
        neigh_list = list(neighbors(node))
        for nxt in reversed(neigh_list):
            if nxt not in seen:
                stack.append(nxt)


def astar(
    start: T,
    is_goal: Callable[[T], bool],
    neighbors: Callable[[T], Iterable[tuple[T, float]]],
    heuristic: Callable[[T], float] | None = None,
) -> tuple[list[T] | None, float]:
    """A* search for weighted graphs.

    neighbors(state) -> iterable of (next_state, step_cost).
    heuristic(state)  -> estimated remaining cost (>=0).
    """
    if heuristic is None:
        def _h(_: T) -> float:
            return 0.0
    else:
        _h = heuristic

    open_heap: list[tuple[float, float, T]] = []
    parent: dict[T, T] = {}
    g: dict[T, float] = {start: 0.0}

    heapq.heappush(open_heap, (_h(start), 0.0, start))

    while open_heap:
        f, g_cur, node = heapq.heappop(open_heap)
        if g_cur != g.get(node, inf):
            continue

        if is_goal(node):
            path = reconstruct_path(parent, node)
            return path, g_cur

        for nxt, cost in neighbors(node):
            new_g = g_cur + cost
            if new_g < g.get(nxt, inf):
                g[nxt] = new_g
                parent[nxt] = node
                heapq.heappush(
                    open_heap,
                    (new_g + _h(nxt), new_g, nxt),
                )

    return None, inf


def build_graph(
    lines: Iterable[str],
    parse_line: Callable[[str], tuple[U, Iterable[U]]],
    *,
    bidirectional: bool = False,
) -> dict[U, list[U]]:
    """Build an adjacency list graph from text lines.

    parse_line(line) -> (node, iterable_of_neighbors)

    bidirectional=True will add reverse edges for each neighbor.
    """
    graph: DefaultDict[U, list[U]] = defaultdict(list)

    for line in lines:
        text = line.strip()
        if not text:
            continue
        node, neighs = parse_line(text)
        for n in neighs:
            graph[node].append(n)
            if bidirectional:
                graph[n].append(node)
        if node not in graph:
            graph[node]  # ensure key exists

    return dict(graph)
