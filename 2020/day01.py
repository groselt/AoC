#! /usr/bin/env python3

from typing import Optional, Set, Tuple

from utils import get_raw_input


def find_two_sum(entries: Set[int], total: int) -> Optional[Tuple[int, int]]:
    for entry in entries:
        other = total - entry
        if other in entries:
            return (entry, other)
    return None


def part1(entries: Set[int]) -> int:
    pair = find_two_sum(entries, 2020)
    return pair[0] * pair[1] if pair else 0


def part2(entries: Set[int]) -> int:
    for entry1 in entries:
        pair = find_two_sum(entries - {entry1}, 2020-entry1)
        if pair:
            return entry1 * pair[0] * pair[1]
    return 0


if __name__ == '__main__':
    raw_input = [int(x) for x in get_raw_input().split()]
    numbers: Set[int] = set(raw_input)
    print(part1(numbers)) # 41979
    print(part2(numbers)) # 193416912
