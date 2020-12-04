#! /usr/bin/env python3

import math
from typing import List

from utils import get_file_lines


def count_trees(map_data: List[str], x_slope: int, y_slope: int) -> int:
    if not data:
        return 0
    result: int = 0
    x, y = 0, 0
    row_len = len(map_data[0])
    while y < len(map_data):
        if data[y][x % row_len] == '#':
            result += 1
        x += x_slope
        y += y_slope
    return result


def part1(map_data: List[str]) -> int:
    return count_trees(map_data, 3, 1)


def part2(map_data: List[str]) -> int:
    return math.prod((
        count_trees(map_data, 1, 1),
        count_trees(map_data, 3, 1),
        count_trees(map_data, 5, 1),
        count_trees(map_data, 7, 1),
        count_trees(map_data, 1, 2)
    ))


if __name__ == '__main__':
    data = get_file_lines()
    print(part1(data))  # 268
    print(part2(data))  # 3093068400
