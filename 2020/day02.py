#! /usr/bin/env python3

from collections import Counter
from typing import NamedTuple, List

from utils import get_file_lines


class PasswordInfo(NamedTuple):
    int1: int
    int2: int
    char: str
    password: str


def parse_password_info(line: str) -> PasswordInfo:
    raw_rule, password = line.split(': ')
    int_rule, char = raw_rule.split()
    int1, int2 = (int(i) for i in int_rule.split('-'))
    return PasswordInfo(int1, int2, char, password)


def part1(password_info: List[PasswordInfo]) -> int:
    result: int = 0
    for info in password_info:
        counter = Counter(info.password)
        if info.char in counter and info.int1 <= counter[info.char] <= info.int2:
            result += 1
    return result


def part2(password_info: List[PasswordInfo]) -> int:
    result: int = 0
    for info in password_info:
        password_len = len(info.password)
        match1 = info.int1 <= password_len and info.password[info.int1-1] == info.char
        match2 = info.int2 <= password_len and info.password[info.int2-1] == info.char
        if match1 ^ match2:
            result += 1
    return result


if __name__ == '__main__':
    data = [parse_password_info(line) for line in get_file_lines()]
    print(part1(data)) # 474
    print(part2(data)) # 745
