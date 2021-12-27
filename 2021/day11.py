#! /usr/bin/env python3.10

from typing import NamedTuple

from utils import get_file_lines


X, Y = 0, 0


class Coord(NamedTuple):
    x: int
    y: int


def _increase_grid(grid: list[list[int]]) -> None:
    for y in range(Y):
        for x in range(X):
            grid[y][x] += 1


def _is_in_bounds(x: int, y: int) -> bool:
    return 0 <= x < X and 0 <= y < Y


def _increase_neighbours(grid: list[list[int]], x: int, y: int) -> list[Coord]:
    if grid[y][x] < 10:
        return []
    grid[y][x] += 1
    new_flashers: list[Coord] = []
    for j in range(y-1, y+2):
        for i in range(x-1, x+2):
            if _is_in_bounds(i, j) and (i != x or j != y) and grid[j][i] < 10:
                grid[j][i] += 1
                if grid[j][i] == 10:
                    new_flashers.append(Coord(i, j))
    return new_flashers


def _prepare_all_to_flash(grid: list[list[int]]) -> None:
    for y in range(Y):
        for x in range(X):
            if grid[y][x] == 10:
                new_flashers = _increase_neighbours(grid, x, y)
                while new_flashers:
                    flasher = new_flashers.pop()
                    new_flashers.extend(_increase_neighbours(grid, flasher.x, flasher.y))


def _flash_all(grid: list[list[int]]) -> int:
    flashes = 0
    for y in range(Y):
        for x in range(X):
            if grid[y][x] > 9:
                flashes += 1
                grid[y][x] = 0
    return flashes


def print_grid(grid: list[list[int]]) -> None:
    for y in range(Y):
        for x in range(X):
            i = grid[y][x]
            print(i if i else '*', end='')
        print()


def part1(grid: list[list[int]], steps: int) -> int:
    flashes = 0
    for i in range(steps):
        _increase_grid(grid)
        _prepare_all_to_flash(grid)
        flashes += _flash_all(grid)
        # print('After step', i+1)
        # print_grid(grid)
        # print()
    return flashes


def part2(grid: list[list[int]]) -> int:
    octopus_count = len(grid) * len(grid[0])
    step = 0
    while True:
        step += 1
        _increase_grid(grid)
        _prepare_all_to_flash(grid)
        if _flash_all(grid) == octopus_count:
            return step


if __name__ == '__main__':
    grid = get_file_lines(transform=lambda line: [int(c) for c in line])
    X, Y = len(grid[0]), len(grid)
    STEPS = 100
    print(part1(grid, STEPS)) # 1719
    print(part2(grid) + STEPS) # 232
