#! /usr/bin/env python3

from typing import List, NamedTuple, Optional, Set

from utils import get_file_lines


def is_valid(preamble, n):
    number_set = set(preamble)
    for i in number_set:
        to_find = n - i
        if to_find != i and to_find in number_set:
            return True
    return False


def part1(numbers) -> int:
    preamble = numbers[:25]
    for n in numbers[25:]:
        if not is_valid(preamble, n):
            return n
        preamble.pop(0)
        preamble.append(n)


def part2(magic, numbers) -> Optional[int]:
    start, end = 0, 1
    while True:
        subset = numbers[start:end+1]
        total = sum(subset)
        if total == magic:
            print(start,end)
            return min(subset) + max(subset)
        if total < magic:
            end += 1
        else:
            start += 1


if __name__ == '__main__':
    raw_numbers = [int(i) for i in get_file_lines()]
    print(part1(raw_numbers))  # 1639024365
    print(part2(1639024365, raw_numbers))  # 219202240
