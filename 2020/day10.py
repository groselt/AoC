#! /usr/bin/env python3

from collections.abc import Iterable
from collections import defaultdict, deque
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
    counter = defaultdict(int)
    last_number = 0
    for next_number in numbers:
        counter[next_number-last_number] += 1
        last_number = next_number
    print(counter)
    return counter[1] * (counter[3] + 1)

# 0   3 4 5   8
# 3 consec: 2 options
# 0   3 4 5 6   9
# 4 consec: 4 options
# 0   3 4 5 6 7   10
# 5 consec: 7
# 0   3 4 5 6 7 8   11
# 6 consec: 14?
def part2(numbers: List[int]) -> int:
    def combos(n: int) -> int:
        optional_bits = n - 1
        return 2**optional_bits - max(optional_bits-2, 0)
    last_number = 0
    runs = []
    running = 0
    for next_number in numbers:
        if next_number-last_number == 1:
            running += 1
        elif running > 0:
            if running >= 2:
                runs.append(combos(running))
            running = 0
        last_number = next_number
    if running >= 2:
        runs.append(combos(running))
    print(runs)
    tot = 1
    for r in runs:
        tot *= r
    return tot


if __name__ == '__main__':
    raw_numbers = sorted([int(i) for i in get_file_lines()])
    print(part1(raw_numbers))  # 2030
    print(part2(raw_numbers))  # 42313823813632
