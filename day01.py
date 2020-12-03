#! /usr/bin/env python3

from typing import Set, Tuple

from utils import get_raw_input


def find_two_sum(entries: Set[int], total: int) -> Tuple[int, int]:
    for e in entries:
        other = total - e
        if other in entries:
            return (e, other)


def part1(entries: Set[int]):
    pair = find_two_sum(entries, 2020)
    return pair[0] * pair[1]


def part2(entries: Set[int]):
    for e1 in entries:
        pair = find_two_sum(entries - {e1}, 2020-e1)
        if pair:
            return e1 * pair[0] * pair[1]


if __name__ == '__main__':
    raw_input = [int(x) for x in get_raw_input().split()]
    entries: Set[int] = set(raw_input)
    print(part1(entries)) # 41979
    print(part2(entries)) # 193416912
