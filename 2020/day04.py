#! /usr/bin/env python3

import re
from typing import Dict, List

from utils import get_file_lines


def parse_passports(raw_lines: List[str]) -> List[Dict]:
    passport = {}
    for line in raw_lines:
        if not line:
            yield passport
            passport = {}
        else:
            pair_strings = [p for p in line.split()]
            fields = { pair.split(':')[0]:pair.split(':')[1] for pair in pair_strings}
            passport.update(fields)
    if passport:
        yield passport


def part1(data: List[Dict]) -> int:
    result: int = 0
    required = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
    for d in data:
        if set(d.keys()).issuperset(required):
            result += 1
    return result


def part2(data: List[str]) -> int:
    result: int = 0
    required = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
    for d in data:
        if set(d.keys()).issuperset(required):
            valid_hgt = (d['hgt'].endswith('cm') and 150 <= int(d['hgt'][:-2]) <= 193) or \
                (d['hgt'].endswith('in') and 59 <= int(d['hgt'][:-2]) <= 76)
            if 1920 <= int(d['byr']) <= 2002 and \
               2010 <= int(d['iyr']) <= 2020 and \
               2020 <= int(d['eyr']) <= 2030 and \
                   valid_hgt and \
               re.match(r'^#\w{6}$', d['hcl']) and \
               d['ecl'] in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth') and \
               re.match(r'^\d{9}$', d['pid']):
                result += 1
    return result


if __name__ == '__main__':
    data = list(parse_passports(get_file_lines()))

    print(part1(data))  # 228
    print(part2(data))  # 175
