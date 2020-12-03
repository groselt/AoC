#! /usr/bin/env python3

from collections import Counter

from utils import get_file_lines


def part1(data) -> int:
    result: int = 0
    for entry in data:
        raw_rule, password = entry
        nr_rule, char = raw_rule.split()
        min_nr, max_nr = (int(nr) for nr in nr_rule.split('-'))
        counter = Counter(password)
        if char in counter and min_nr <= counter[char] <= max_nr:
            result += 1
    return result


def part2(data) -> int:
    result: int = 0
    for entry in data:
        raw_rule, password = entry
        pos_rule, char = raw_rule.split()
        pos1, pos2 = (int(nr) for nr in pos_rule.split('-'))
        password_len = len(password)
        match1 = pos1 <= password_len and password[pos1-1] == char
        match2 = pos2 <= password_len and password[pos2-1] == char
        if match1 ^ match2:
                result += 1
    return result


if __name__ == '__main__':
    raw_input = [line.split(': ') for line in get_file_lines()]
    print(part1(raw_input)) # 474
    print(part2(raw_input)) # 745
