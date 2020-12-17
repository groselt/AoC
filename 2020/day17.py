#! /usr/bin/env python3

from collections import defaultdict
import itertools
from typing import Dict, Iterable, List, Tuple

from utils import get_file_lines


Coord = Tuple[int, ...]
Cube = Dict[Coord, bool]


def parse_raw_data(lines: List[str], dimensions: int) -> Cube:
    cube: Cube = defaultdict(bool)
    for y, line in enumerate(lines):
        for x, state in enumerate(line):
            if state == '#':
                cube[(x, y) + (0,) * (dimensions - 2)] = True
    return cube


def get_boundaries(cube: Cube, dimensions: int) -> Tuple[Coord, Coord]:
    min_coord = [999] * dimensions
    max_coord = [-999] * dimensions
    for coord in cube:
        for d in range(dimensions):
            min_coord[d] = min(coord[d], min_coord[d])
            max_coord[d] = max(coord[d], max_coord[d])
    return (tuple(min_coord), tuple(max_coord))


def get_all_coordinates(min_coord: Coord, max_coord: Coord, dimensions: int) -> Iterable[Coord]:
    ranges = [range(min_coord[d]-1, max_coord[d]+2) for d in range(dimensions)]
    for permutation in itertools.product(*ranges):
        yield tuple(permutation)


def get_neighbours(coord: Coord, dimensions: int) -> Iterable:
    for neighbour in get_all_coordinates(coord, coord, dimensions):
        if neighbour != coord:
            yield neighbour


def should_activate(status: bool, neighbour_count: int) -> bool:
    return status and neighbour_count in (2, 3) or \
        not status and neighbour_count == 3


def next_gen(cube: Cube, dimensions: int) -> Cube:
    next_cube: Cube = defaultdict(bool)
    min_coord, max_coord = get_boundaries(cube, dimensions)
    for coord in get_all_coordinates(min_coord, max_coord, dimensions):
        neighbour_count = 0
        for neighbour in get_neighbours(coord, dimensions):
            if cube[neighbour]:
                neighbour_count += 1
        if should_activate(cube[coord], neighbour_count):
            next_cube[coord] = True
    return next_cube


def part1(cube: Cube) -> int:
    for _ in range(6):
        cube = next_gen(cube, 3)
    return sum(state for state in cube.values())


def part2(cube: Cube) -> int:
    for _ in range(6):
        cube = next_gen(cube, 4)
    return sum(state for state in cube.values())


if __name__ == '__main__':
    raw_data = get_file_lines()

    initial_map_3d = parse_raw_data(raw_data, 3)
    print(part1(initial_map_3d))  # 240

    initial_map_4d = parse_raw_data(raw_data, 4)
    print(part2(initial_map_4d))  # 1180
