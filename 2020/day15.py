#! /usr/bin/env python3

from collections import defaultdict
from typing import Dict, List

from utils import get_file_lines


def calc_nth(data: List[int], nth: int) -> int:
    def get_prev_pos(num: int):
        if len(all_numbers.get(num, [])) <= 1:
            return -1
        return all_numbers[num][-2]
    all_numbers: Dict[int, List[int]] = defaultdict(list)  # {num: [turn]}
    for i, num in enumerate(data):
        all_numbers[num] = [i+1]
    prev = data[-1]
    start_len = len(data)
    for i in range(start_len, nth):
        prev_pos = get_prev_pos(prev)
        if prev_pos == -1:
            new = 0
        else:
            new = i - prev_pos
        all_numbers[new].append(i+1)
        prev = new
    return prev


def part1(data: List[int]) -> int:
    return calc_nth(data, 2020)


def part2(data: List[int]) -> int:
    return calc_nth(data, 30_000_000)


if __name__ == '__main__':
    raw_data = [int(x) for x in get_file_lines()[0].split(',')]
    print(part1(raw_data))  # 1618
    print(part2(raw_data))  # 548531
