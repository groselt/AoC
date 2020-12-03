#! /usr/bin/env python3

import math
from typing import List

from utils import get_file_lines


def count_trees(data: List[str], dx: int, dy: int) -> int:
    result: int = 0
    x, y = 0, 0
    row_len = None if not data else len(data[0])
    while y < len(data):
        if data[y][x%row_len] == '#':
            result += 1
        x += dx
        y += dy
    return result


def part1(data: List[str]) -> int:
    return count_trees(data, 3, 1)


def part2(data: List[str]) -> int:
    return math.prod((
        count_trees(data, 1, 1),
        count_trees(data, 3, 1),
        count_trees(data, 5, 1),
        count_trees(data, 7, 1),
        count_trees(data, 1, 2)
    ))


if __name__ == '__main__':
    data = get_file_lines()
    print(part1(data))  # 268
    print(part2(data))  # 3093068400
