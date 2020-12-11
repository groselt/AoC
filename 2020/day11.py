#! /usr/bin/env python3

from itertools import chain
from typing import List

from utils import get_file_lines


NEIGHBOUR_DIRS = ((-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1))


def get_nr_occupied_neighbours(floor_map: List[str], x: int, y:int, max_depth: int) -> int:
    row_count = len(floor_map)
    col_count = len(floor_map[0])
    result: int = 0
    for i, j in NEIGHBOUR_DIRS:
        neighbour_found, is_in_bounds = False, True
        depth = 1
        while is_in_bounds and not neighbour_found and depth <= max_depth:
            is_in_bounds = 0 <= (neighbour_y := y + j*depth) < row_count and \
                           0 <= (neighbour_x := x + i*depth) < col_count
            if is_in_bounds:
                if floor_map[neighbour_y][neighbour_x] == '.':
                    depth += 1
                else:
                    neighbour_found = True
        if neighbour_found and floor_map[neighbour_y][neighbour_x] == '#':
            result += 1
    return result


def generate_next(
        floor_map: List[str],
        max_neighbour_depth: int,
        neighbour_threshold: int) -> List[str]:
    def _get_nr_occupied_neighbours(x: int, y: int) -> int:
        return get_nr_occupied_neighbours(floor_map, x, y, max_neighbour_depth)
    def _too_many_neighbours(x: int, y: int) -> bool:
        return _get_nr_occupied_neighbours(x, y) >= neighbour_threshold
    result: List[str] = []
    for y in range(len(floor_map)):
        new_row = ''
        for x in range(len(floor_map[0])):
            if floor_map[y][x] == 'L' and _get_nr_occupied_neighbours(x, y) == 0:
                new_row += '#'
            elif floor_map[y][x] == '#' and _too_many_neighbours(x, y):
                new_row += 'L'
            else:
                new_row += floor_map[y][x]
        result.append(new_row)
    return result


def part1(floor_map: List[str]) -> int:
    neighbour_depth = 1
    neighbour_threshold = 4
    old_map = floor_map
    while (new_map := generate_next(old_map, neighbour_depth, neighbour_threshold)) != old_map:
        old_map = new_map
    return sum(x=='#' for x in chain.from_iterable(old_map))


def part2(floor_map: List[str]) -> int:
    neighbour_depth = max(len(floor_map), len(floor_map[0]))
    neighbour_threshold = 5
    old_map = floor_map
    while (new_map := generate_next(old_map, neighbour_depth, neighbour_threshold)) != old_map:
        old_map = new_map
    return sum(x=='#' for x in chain.from_iterable(old_map))


if __name__ == '__main__':
    raw_map = get_file_lines()
    print(part1(raw_map))  # 2481
    print(part2(raw_map))  # 2227
