#! /usr/bin/env python3

from typing import Dict, Iterable, List

from utils import get_file_lines


DIRECTIONS = {
    'w': -2,
    'e': 2,
    'nw': -1+1j,
    'sw': -1-1j,
    'ne': 1+1j,
    'se': 1-1j
}


def get_initial_state(all_moves: List[str]) -> Dict[complex, int]:
    floor: Dict[complex, int] = dict()  # {position: 0/1} 0=white, black=1
    for moves in all_moves:
        position = complex()
        while moves:
            for name, change in DIRECTIONS.items():
                if moves.startswith(name):
                    position += change
                    moves = moves[len(name):]
        floor[position] = (floor.get(position, 0) + 1) % 2
    return floor


def get_neighbours(position: complex) -> Iterable:
    for direction in DIRECTIONS.values():
        yield position + direction


def count_black_neighbours(floor: Dict[complex, int], position: complex) -> int:
    return sum(floor.get(pos, 0) for pos in get_neighbours(position))


def next_floor(floor: Dict[complex, int]) -> Dict[complex, int]:
    minx = int(min(pos.real for pos in floor.keys()))
    miny = int(min(pos.imag for pos in floor.keys()))
    maxx = int(max(pos.real for pos in floor.keys()))
    maxy = int(max(pos.imag for pos in floor.keys()))
    new_floor: Dict[complex, int] = dict()
    for x in range(minx-2, maxx+3):
        for y in range(miny-2, maxy+3):
            position = complex(x, y)
            tile = floor.get(position, 0)
            black = count_black_neighbours(floor, position)
            if tile == 1 and black in (1, 2):
                new_floor[position] = 1
            elif tile == 0 and black == 2:
                new_floor[position] = 1
    return new_floor


def part1(floor: Dict[complex, int]) -> int:
    return sum(floor.values())


def part2(floor: Dict[complex, int]) -> int:
    for _ in range(100):
        floor = next_floor(floor)
    return sum(floor.values())


if __name__ == '__main__':
    raw_data = get_file_lines()
    raw_floor = get_initial_state(raw_data)
    print(part1(raw_floor))  # 394
    print(part2(raw_floor))  # 4036
