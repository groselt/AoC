#! /usr/bin/env python3.10

import heapq
from typing import Iterable

from utils import get_file_lines


START = (0, 0)
FINISH = (-1, -1)


def in_range(x: int, y: int) -> bool:
    return 0 <= x <= FINISH[0] and 0 <= y <= FINISH[1]


def neighbours(pos: tuple[int, int]) -> Iterable[tuple[int, int]]:
    x, y = pos
    deltas = ((-1, 0), (0, -1), (1, 0), (0, 1))
    for delta in deltas:
        new_x, new_y = x + delta[0], y + delta[1]
        if in_range(new_x, new_y):
            yield (new_x, new_y)


def pos_risk(grid: list[list[int]], x: int, y: int) -> int:
    tile_width = len(grid)
    risk = grid[y % tile_width][x % tile_width]
    if x >= tile_width or y >= tile_width:
        risk = (risk - 1 + x // tile_width + y // tile_width) % 9 + 1
    return risk


def find_shortest_path(grid: list[list[int]], scale: int) -> int:
    tile_width = len(grid)
    global FINISH
    FINISH = (tile_width*scale-1, tile_width*scale-1)
    current, end = START, FINISH
    visited = set()
    heap = []
    heapq.heappush(heap, (0, current))  # total risk, position
    while heap:
        risk, pos = heapq.heappop(heap)
        for neighbour in neighbours(pos):
            if not neighbour in visited:
                visited.add(neighbour)
                x, y = neighbour
                new_risk = risk + pos_risk(grid, x, y)
                if neighbour == end:
                    return new_risk
                heapq.heappush(heap, (new_risk, neighbour))
    raise RuntimeError('Destination not reached')


def part1(grid: list[list[int]]) -> int:
    return find_shortest_path(grid, 1)


def part2(grid: list[list[int]]) -> int:
    return find_shortest_path(grid, 5)


if __name__ == '__main__':
    lines = get_file_lines()
    grid = []
    for line in lines:
        grid.append([int(c) for c in line])
    FINISH = (len(grid)-1, len(grid)-1)
    print(part1(grid)) # 745
    print(part2(grid)) # 3002
