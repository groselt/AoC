#! /usr/bin/env python3

from itertools import chain
from typing import List

from utils import get_file_lines


def p1_get_nr_occupied_neighbours(floor_map: List[str], x: int, y:int) -> int:
    def is_safe(x,y) -> bool:
        return 0 <= y < len(floor_map) and 0 <= x < len(floor_map[y])
    result: int = 0
    positions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    for i, j in positions:
        if is_safe(x+i, y+j) and floor_map[y+j][x+i] == '#':
            result += 1
    return result


def p2_get_nr_occupied_neighbours(floor_map: List[str], x: int, y:int) -> int:
    def is_safe(x,y) -> bool:
        return 0 <= y < len(floor_map) and 0 <= x < len(floor_map[y])
    result: int = 0
    positions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    for i, j in positions:
        depth = 1
        while is_safe(x+i*depth, y+j*depth) and floor_map[y+j*depth][x+i*depth] == '.':
            depth += 1
        if is_safe(x+i*depth, y+j*depth) and floor_map[y+j*depth][x+i*depth] == '#':
            result += 1
    return result


def p1_generate_next(floor_map: List[str]) -> List[str]:
    result: List[str] = []
    for y in range(len(floor_map)):
        new_row = ''
        for x in range(len(floor_map[0])):
            neighbours = p1_get_nr_occupied_neighbours(floor_map, x,y)
            if floor_map[y][x] == 'L' and neighbours == 0:
                new_row += '#'
            elif floor_map[y][x] == '#' and neighbours >= 4:
                new_row += 'L'
            else:
                new_row += floor_map[y][x]
        result.append(new_row)
    return result


def p2_generate_next(floor_map: List[str]) -> List[str]:
    result: List[str] = []
    for y in range(len(floor_map)):
        new_row = ''
        for x in range(len(floor_map[0])):
            neighbours = p2_get_nr_occupied_neighbours(floor_map, x,y)
            if floor_map[y][x] == 'L' and neighbours == 0:
                new_row += '#'
            elif floor_map[y][x] == '#' and neighbours >= 5:
                new_row += 'L'
            else:
                new_row += floor_map[y][x]
        result.append(new_row)
    return result


def part1(floor_map: List[str]) -> int:
    old_map = floor_map
    while True:
        new_map = p1_generate_next(old_map)
        if new_map == old_map:
            break
        old_map = new_map
    return sum(x=='#' for x in chain.from_iterable(old_map))


def part2(floor_map: List[str]) -> int:
    old_map = floor_map
    while True:
        new_map = p2_generate_next(old_map)
        if new_map == old_map:
            break
        old_map = new_map
    return sum(x=='#' for x in chain.from_iterable(old_map))

if __name__ == '__main__':
    raw_map = get_file_lines()
    print(part1(raw_map))  # 2481
    print(part2(raw_map))  # 2227
