#! /usr/bin/env python3

from typing import List

from utils import get_file_lines


def calc_nth(data: List[int], nth: int) -> int:
    all_numbers = { num: index + 1 for index, num in enumerate(data) }  # num: previous index
    previous = data[-1]
    for i in range(len(data), nth):
        previous_index = all_numbers.get(previous, i)
        new_number = i - previous_index
        all_numbers[previous] = i
        previous = new_number
    return previous


def part1(data: List[int]) -> int:
    return calc_nth(data, 2020)


def part2(data: List[int]) -> int:
    return calc_nth(data, 30_000_000)


if __name__ == '__main__':
    raw_data = [int(x) for x in get_file_lines()[0].split(',')]
    print(part1(raw_data))  # 1618
    print(part2(raw_data))  # 548531
