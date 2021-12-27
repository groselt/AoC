#! /usr/bin/env python3.10

from collections import Counter, defaultdict
from itertools import chain, pairwise
from typing import Tuple

from utils import get_file_lines


def parse_lines(lines: list[str]) -> Tuple[str, dict]:
    template = lines[0]
    rules = {pair: new for pair, new in [line.split(' -> ') for line in lines[2:]]}

    return template, rules


def polymerise(template: str, rules: map) -> str:
    additions = ''
    for a, b in pairwise(template):
        additions += rules[a+b]
    return list(chain.from_iterable(zip(template, additions+'_')))[:-1]


def update_occurrences(pair_counts: defaultdict, rules: map) -> None:
    new_pair_counts = defaultdict(int)
    for pair, count in pair_counts.items():
        new = rules[pair]
        new_pair_counts[pair[0]+new] += count
        new_pair_counts[new+pair[1]] += count
    pair_counts.clear()
    pair_counts.update(new_pair_counts)


def part1(template: str, rules: map) -> int:
    for _ in range(10):
        template = polymerise(template, rules)
    count = Counter(template)
    all_elements = count.most_common()
    return all_elements[0][1] - all_elements[-1][1]


def part2(template: str, rules: map) -> int:
    pair_counts = defaultdict(int)
    for a, b in pairwise(template):
        pair_counts[a+b] += 1

    for _ in range(40):
        update_occurrences(pair_counts, rules)

    counter = defaultdict(int)
    for pair, count in pair_counts.items():
        counter[pair[0]] += count
        counter[pair[1]] += count
    # Items got counted twice, except for first and last, so double them too
    counter[template[0]] += 1
    counter[template[-1]] += 1
    return (max(counter.values()) - min(counter.values())) // 2


if __name__ == '__main__':
    lines = get_file_lines()
    template, rules = parse_lines(lines)
    print(part1(template, rules)) # 2233
    print(part2(template, rules)) # 2884513602164
