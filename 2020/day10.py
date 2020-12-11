#! /usr/bin/env python3

from collections import defaultdict
import math
from typing import DefaultDict, List

from utils import get_file_lines


def part1(numbers: List[int]) -> int:
    counter: DefaultDict[int, int] = defaultdict(int)
    last_number = 0
    for next_number in numbers:
        counter[next_number-last_number] += 1
        last_number = next_number
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
    ''' When more than 2 consecutive numbers (group) present, the middle ones are redundant.
        These middle numbers are redundant as long as we don't omit more than
        two consecutive middle numbers
        Number of combinations is determined by considering each middle number as a bit
        which can be present (one) or not (zero): s**nrOfBits. Then subtract the number
        of groups of 3 consecutive bits: nrBits-2'''
    def are_consecutive(first: int, second: int) -> bool:
        return second - first == 1
    def combinations(nr_middle_bits: int) -> int:
        return 2**nr_middle_bits - max(nr_middle_bits-2, 0)
    last_number = 0
    group_combinations: List[int] = []  # nr combinations for each consecutive group
    length = 0
    for next_number in numbers:
        if are_consecutive(last_number, next_number):
            length += 1
        elif length > 0:
            if length >= 2:
                group_combinations.append(combinations(length - 1))
            length = 0
        last_number = next_number
    if length >= 2:
        group_combinations.append(combinations(length))
    return math.prod(group_combinations)


if __name__ == '__main__':
    raw_numbers = sorted([int(i) for i in get_file_lines()])
    print(part1(raw_numbers))  # 2030
    print(part2(raw_numbers))  # 42313823813632
