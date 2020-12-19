#! /usr/bin/env python3

import re
from typing import Dict, List

from utils import get_file_lines


def parse_rules_list(lines: List[str]) -> Dict[int, str]:
    rules: Dict[int, str] = dict()
    for line in lines:
        index, rule = line.split(': ')
        rules[int(index)] = rule
    return rules


def get_pattern(rules: Dict[int, str], index: int, max_msg_len: int) -> str:
    if max_msg_len == 0:
        return ''
    rule = rules[index]
    if '"' in rule:
        return rule[1]

    pattern_options = []
    options = rule.split(' | ')
    for option in options:
        sub_rules = map(int, option.split())
        pattern_options.append(''.join(get_pattern(rules, i, max_msg_len-1) for i in sub_rules))

    return '(' + '|'.join(pattern_options) + ')'


def part1(rules: Dict[int, str], messages: List[str]) -> int:
    max_message_length = max(len(m) for m in raw_messages)
    pattern = '^' + get_pattern(rules, 0, max_message_length) + '$'
    regex = re.compile(pattern)
    return sum(regex.match(message) is not None for message in messages)


def part2(rules: Dict[int, str], messages: List[str]) -> int:
    rules[8] = '42 | 42 8'
    rules[11] = '42 31 | 42 11 31'
    max_message_length = max(len(m) for m in raw_messages)
    pattern = '^' + get_pattern(rules, 0, max_message_length) + '$'
    regex = re.compile(pattern)
    return sum(regex.match(message) is not None for message in messages)


if __name__ == '__main__':
    raw_data = get_file_lines()
    split = raw_data.index('')
    raw_rules = parse_rules_list(raw_data[:split])
    raw_messages = raw_data[split+1:]

    print(part1(raw_rules, raw_messages))  # 144
    print(part2(raw_rules, raw_messages))  # 260
