from __future__ import annotations

from typing import Any

from re import findall
#from itertools import combinations, permutations, product
#from math import prod, lcm, ceil, floor, gcd

from aoc.progress import prog # Add a progress bar when needed (used as enumerate)

#from aoc.grid import NORTH, SOUTH, EAST, WEST, DIR4, neighbors4, parse_char_grid,
#  parse_int_grid, add_pos, UP, DOWN, LEFT, RIGHT, in_bounds
#from aoc.grid import NORTH, SOUTH, EAST, WEST, DIR8, neighbors8, parse_char_grid,
#  NORTH_EAST as NE, NORTH_WEST as NW, SOUTH_EAST as SE, SOUTH_WEST as SW
from aoc.search import bfs_one, dijkstra_one
#from aoc.iteration import split_by, unique_permutations, nwise

from aoc.common import read_input, time_call
from aoc.config import AOC_YEAR

DAY = 10


def parse_input(raw: str) -> Any:
    """Convert the raw text into a convenient structure."""
    input = raw.rstrip("\n").splitlines()
    re = r"^\[([.#]+)\] (\(.+\)) \{(.+)\}$"
    machines = [findall(re, l)[0] for l in input]
    out = []
    for lights, buttons, joltage in machines:
        lights = [c == "#" for c in lights]
        buttons = [(int(a) for a in l.strip("()").split(","))
                   for l in findall(r"\([0-9,]+\)", buttons)]
        joltage = [int(a) for a in  joltage.split(",")]
        out.append((lights, buttons, joltage))
    return out


def part1(data: Any) -> Any:
    """Solve part 1."""

    machines = []
    for lights, bts,_ in data:
        mod = 2**len(lights)
        lights = sum(int(l)*(2**n) for n, l in enumerate(lights))
        bts = [sum(2**n for n in b) for b in bts]
        machines.append((mod, lights, bts))
    
    #print(machines)

    def neighbor(mod, bts):
        def _neigh(lights):
            for btn in bts:
                yield (lights^btn) % mod
        return _neigh

    def fewest_presses(mod, lights, bts):
        return bfs_one(
            start=0,
            neighbors=neighbor(mod, bts),
            is_goal=lambda x: x == lights
        )

    #zum = 0
    #for i, (m,l,b) in enumerate(machines):
    #    n = fewest_presses(m,l,b)
    #    print(i, m,l,b, n.goal_cost(), n.path_to_goal())
    #    zum += n.goal_cost()

    return sum(fewest_presses(m,l,b).goal_cost() for m,l,b in machines) 


def part2(data: Any) -> Any:
    """Solve part 2."""

    def fewest_presses(buttons, joltages):
        value = sum(joltages)
        #print(value)

        # For each joltage dial, find the buttons that can manipulate it
        j_bts = [set() for i, _ in enumerate(joltages)]

        # bts_max: For each btn, find the max number of times it can be pressed
        # bts_val: For each btn, the number of joltages it will increase (len)
        bts_max = {}
        bts_val = {}
        for i, btn in enumerate(buttons):
            btn_max = 10**6
            bts_val[i] = len(btn)
            for j, dial in enumerate(btn):
               j_bts[dial].add(i)
               btn_max = min(joltages[dial], btn_max)
            bts_max[i] = btn_max

        #print(j_bts, bts_max)

        # Possible minor optimization:
        #for j, bts in enumerate(j_bts):
        #    if len(bts) == 1: pass # We know that only one button can set this dial

        # Now, we know that number of btn presses must equal the dial settings
        #
        # for btn a->d and dial x,y,z,q
        # x = a + b
        # y = b + c + d
        # z = a + d
        # q = b + d
        # min(a+b+c+d)

        # Let's try dijkstra. The edge cost will be max -bts_val(i)
        # So we greedily push the button that increments the most dials first
        # But we don't care about order... so x y x y == y x y x (order of pushes)

        start = (0,) * len(buttons)
        #print(buttons)

        def check_press(node, goal = False):
            for dial, bts in enumerate(j_bts):
                #print(node, bts)
                dial_val = sum(node[i] for i in bts)
                if dial_val > joltages[dial]: return False
                if goal and dial_val < joltages[dial]: return False
            return True

        def neighbor(node):
            for i, btn in enumerate(buttons):
                if bts_max[i] < node[i] + 1: continue
                nxt = node[:i] + (node[i] + 1,) + node[i+1:]
                if sum(bts_val[n]*j for n, j in enumerate(node)) > value: continue
                if check_press(nxt):
                    yield tuple(nxt), -bts_val[i]
        
        return sum(dijkstra_one(start, neighbor, lambda x: check_press(x, goal=True)).goal)

    zum = 0
    for n, (_,b,j) in prog(data):
        buttons = tuple(list(a) for  a in b)
        zum += fewest_presses(tuple(buttons),tuple(j))
                
    return zum


def main() -> None:
    raw = read_input(DAY)
    data = parse_input(raw)

    p1 = time_call(part1, data)
    print(f"Year {AOC_YEAR} Day {DAY} - Part 1: {p1.value} ({p1.seconds:.3f}s)")

    raw = read_input(DAY)
    data = parse_input(raw)

    p2 = time_call(part2, data)
    print(f"Year {AOC_YEAR} Day {DAY} - Part 2: {p2.value} ({p2.seconds:.3f}s)")


if __name__ == "__main__":
    main()
