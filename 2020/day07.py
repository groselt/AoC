#! /usr/bin/env python3

import re
from typing import Dict, List, NamedTuple

from utils import get_file_lines


class Capacity(NamedTuple):
    colour: str
    count: int


def load_bag_rules(lines):
    rules = dict()  # {colour: [Capacity]}
    parent_pattern = re.compile(r'(\w+ \w+) bags contain (.+)\.')
    child_pattern = re.compile(r'(\d+) (\w+ \w+) bags?,?')
    for line in lines:
        match = parent_pattern.match(line)
        parent = match.group(1)
        children = []
        for child in child_pattern.findall(match.group(2)):
            children.append(Capacity(child[1], int(child[0])))
        rules[parent] = children
    return rules


def can_bag_contain_colour(rules, source_colour, target_colour):
    for child in rules[source_colour]:
        if child.colour == target_colour:
            return True
        if can_bag_contain_colour(rules, child.colour, target_colour):
            return True
    return False


def count_contained(rules, colour):
    if not rules[colour]:
        return 1
    result: int = 1
    for child in rules[colour]:
        cnt = count_contained(rules, child.colour)
        result += child.count * cnt
    return result


def part1(rules: Dict[str, List[Capacity]]) -> int:
    return sum(can_bag_contain_colour(rules, b, 'shiny gold') for b in rules.keys())


def part2(rules: Dict[str, List[Capacity]]) -> int:
    return count_contained(rules, 'shiny gold') - 1


if __name__ == '__main__':
    raw_data = get_file_lines()
    bag_rules = load_bag_rules(raw_data)
    print(part1(bag_rules))  # 142
    print(part2(bag_rules))  # 10219
