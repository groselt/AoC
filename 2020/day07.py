#! /usr/bin/env python3

import re
from typing import Dict, List, NamedTuple, Tuple

from utils import get_file_lines


class Capacity(NamedTuple):
    total: int
    colour: str


def parse_rule(line: str) -> Tuple[str, List[Capacity]]:
    parent_pattern = re.compile(r'(\w+ \w+) bags contain (.+)\.')
    child_pattern = re.compile(r'(\d+) (\w+ \w+) bags?,?')
    parent, raw_children = parent_pattern.match(line).groups()  # type: ignore
    return (
        parent,
        [Capacity(int(child[0]), child[1]) for child in child_pattern.findall(raw_children)]
    )


def can_bag_contain_colour(rules: Dict[str, List[Capacity]],
                           source_colour: str,
                           target_colour: str) -> bool:
    return any(
        child.colour == target_colour or
        can_bag_contain_colour(rules, child.colour, target_colour)
        for child in rules[source_colour]
    )


def count_contained(rules: Dict[str, List[Capacity]], colour: str) -> int:
    return sum(
        (child.total *
         count_contained(rules, child.colour) for child in rules[colour]),
        1
    )


def part1(rules: Dict[str, List[Capacity]]) -> int:
    return sum(can_bag_contain_colour(rules, b, 'shiny gold') for b in rules.keys())


def part2(rules: Dict[str, List[Capacity]]) -> int:
    return count_contained(rules, 'shiny gold') - 1  # exclude the bag itself


if __name__ == '__main__':
    bag_rules = dict(parse_rule(line) for line in get_file_lines())
    print(part1(bag_rules))  # 142
    print(part2(bag_rules))  # 10219
