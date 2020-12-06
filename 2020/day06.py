#! /usr/bin/env python3

from collections import Counter
import itertools
from typing import List

from utils import get_file_lines


def group_data(raw_lines: List[str]) -> List[List[str]]:
    result: List[List[str]] = [[]]
    for line in raw_lines:
        if not line:
            result.append([])
        else:
            result[-1].append(line)
    return result


def part1(groups: List[List[str]]) -> int:
    return sum(len(Counter(itertools.chain.from_iterable(g))) for g in groups)


def part2(groups: List[List[str]]) -> int:
    result: int = 0
    for group in groups:
        counts = Counter(itertools.chain.from_iterable(group))
        result += sum(v == len(group) for v in counts.values())
    return result


if __name__ == '__main__':
    raw_data = get_file_lines()
    grouped_data = group_data(raw_data)
    print(part1(grouped_data))  # 6809
    print(part2(grouped_data))  # 3394
