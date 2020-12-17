#! /usr/bin/env python3

from collections import defaultdict
import math
from typing import Dict, Iterable, List, Optional, Tuple

from utils import get_file_lines


Coord_3D = Tuple[int, int, int]
Cube_3D = Dict[Coord_3D, bool]
Coord_4D = Tuple[int, int, int, int]
Cube_4D = Dict[Coord_4D, bool]


def parse_raw_data_3D(lines: List[str]) -> Cube_3D:
    cube: Cube_3D = defaultdict(bool)
    for y, line in enumerate(lines):
        for x, state in enumerate(line):
            if state == '#':
                cube[(x, y, 0)] = True
    return cube


def parse_raw_data_4D(lines: List[str]) -> Cube_4D:
    cube: Cube_4D = defaultdict(bool)
    for y, line in enumerate(lines):
        for x, state in enumerate(line):
            if state == '#':
                cube[(x, y, 0, 0)] = True
    return cube


def get_boundaries_3D(cube: Cube_3D) -> Tuple[Coord_3D, Coord_3D]:
    min_coord = (999, 999, 999)
    max_coord = (-999, -999, -999)
    for coord in cube:
        min_x = min(coord[0], min_coord[0])
        min_y = min(coord[1], min_coord[1])
        min_z = min(coord[2], min_coord[2])
        max_x = max(coord[0], max_coord[0])
        max_y = max(coord[1], max_coord[1])
        max_z = max(coord[2], max_coord[2])
        min_coord = (min_x, min_y, min_z)
        max_coord = (max_x, max_y, max_z)
    return (min_coord, max_coord)
    

def get_boundaries_4D(cube: Cube_4D) -> Tuple[Coord_4D, Coord_4D]:
    min_coord = (999, 999, 999, 999)
    max_coord = (-999, -999, -999, -999)
    for coord in cube:
        min_x = min(coord[0], min_coord[0])
        min_y = min(coord[1], min_coord[1])
        min_z = min(coord[2], min_coord[2])
        min_w = min(coord[3], min_coord[3])
        max_x = max(coord[0], max_coord[0])
        max_y = max(coord[1], max_coord[1])
        max_z = max(coord[2], max_coord[2])
        max_w = max(coord[3], max_coord[3])
        min_coord = (min_x, min_y, min_z, min_w)
        max_coord = (max_x, max_y, max_z, max_w)
    return (min_coord, max_coord)


def get_neighbours_3D(coord: Coord_3D) -> Iterable:
    for x in range(coord[0]-1, coord[0]+2):
        for y in range(coord[1]-1, coord[1]+2):
            for z in range(coord[2]-1, coord[2]+2):
                neighbour = (x, y, z)
                if neighbour != coord:
                    yield neighbour


def get_neighbours_4D(coord: Coord_4D) -> Iterable:
    for x in range(coord[0]-1, coord[0]+2):
        for y in range(coord[1]-1, coord[1]+2):
            for z in range(coord[2]-1, coord[2]+2):
                for w in range(coord[3]-1, coord[3]+2):
                    neighbour = (x, y, z, w)
                    if neighbour != coord:
                        yield neighbour


def next_gen_3D(cube: Cube_3D) -> Cube_3D:
    next_cube = defaultdict(bool)
    min_coord, max_coord = get_boundaries_3D(cube)
    for x in range(min_coord[0]-1, max_coord[0]+2):
        for y in range(min_coord[1]-1, max_coord[1]+2):
            for z in range(min_coord[2]-1, max_coord[2]+2):
                current = (x, y, z)
                neighbour_count = 0
                for neighbour in get_neighbours_3D(current):
                    if cube[neighbour]:
                        neighbour_count += 1
                if cube[current] and neighbour_count in (2, 3) or \
                   not cube[current] and neighbour_count == 3:
                    next_cube[current] = True
    return next_cube


def next_gen_4D(cube: Cube_4D) -> Cube_4D:
    next_cube = defaultdict(bool)
    min_coord, max_coord = get_boundaries_4D(cube)
    for x in range(min_coord[0]-1, max_coord[0]+2):
        for y in range(min_coord[1]-1, max_coord[1]+2):
            for z in range(min_coord[2]-1, max_coord[2]+2):
                for w in range(min_coord[3]-1, max_coord[3]+2):
                    current = (x, y, z, w)
                    neighbour_count = 0
                    for neighbour in get_neighbours_4D(current):
                        if cube[neighbour]:
                            neighbour_count += 1
                    if cube[current] and neighbour_count in (2, 3) or \
                    not cube[current] and neighbour_count == 3:
                        next_cube[current] = True
    return next_cube


def part1(cube: Cube_3D) -> int:
    for _ in range(6):
        cube = next_gen_3D(cube)
    return sum(state for state in cube.values())


def part2(cube: Cube_4D) -> int:
    for _ in range(6):
        cube = next_gen_4D(cube)
    print(cube)
    return sum(state for state in cube.values())


if __name__ == '__main__':
    raw_data = get_file_lines()
    initial_map_3D = parse_raw_data_3D(raw_data)
    print(part1(initial_map_3D))  # 240
    initial_map_4D = parse_raw_data_4D(raw_data)
    print(part2(initial_map_4D))  # 1180
