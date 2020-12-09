#! /usr/bin/env python3

from collections.abc import Iterable
from collections import deque
from typing import Callable, Deque, List

from utils import get_file_lines


def is_valid(preamble: Deque[int], total: int) -> bool:
    preamble_set = set(preamble)
    for first_number in preamble_set:
        other_number = total - first_number
        if other_number != first_number and other_number in preamble_set:
            return True
    return False


def part1(numbers: List[int]) -> int:
    preamble = deque(numbers[:25])
    for next_number in numbers[25:]:
        if not is_valid(preamble, next_number):
            return next_number
        preamble.popleft()
        preamble.append(next_number)
    return 0


def part2(numbers: List[int], magic_number: int) -> int:
    def apply_range(
            fn: Callable[[Iterable], int],
            first_index: int,
            last_index: int):
        return fn(numbers[i] for i in range(first_index, last_index+1))

    start, end = 0, 1
    while True:
        total = apply_range(sum, start, end)
        if total == magic_number:
            return apply_range(min, start, end) + apply_range(max, start, end)
        if total < magic_number:
            end += 1
        else:
            start += 1


if __name__ == '__main__':
    raw_numbers = [int(i) for i in get_file_lines()]
    print(magic := part1(raw_numbers))  # 1639024365
    print(part2(raw_numbers, magic))  # 219202240
