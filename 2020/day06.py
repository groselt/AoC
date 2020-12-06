#! /usr/bin/env python3

from collections import Counter
from typing import List

from utils import get_file_lines


def group_data(raw_data: List[str]) -> List[str]:
    result = []
    group = []
    for line in raw_data:
        if not line:
            result.append(group)
            group = []
        else:
            group.append(line)
    if group:
        result.append(group)
    return result


def part1(groups: List[List[str]]) -> int:
    result = 0
    for group in groups:
        answers = [x for g in group for x in g]
        result += len(Counter(answers))
    return result
    

def part2(groups: List[List[str]]) -> int:
    result = 0
    for group in groups:
        answers = [x for g in group for x in g]
        counts = Counter(answers)
        result += sum(1 for v in counts.values() if v == len(group))
    return result


if __name__ == '__main__':
    raw_data = get_file_lines()
    group_data = group_data(raw_data)
    print(part1(group_data))  # 6809
    print(part2(group_data))  # 3394
