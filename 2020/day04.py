#! /usr/bin/env python3

import re
from typing import Dict, Iterable, List

from utils import get_file_lines


REQUIRED_FIELDS = {
    'byr': lambda x: 1920 <= int(x) <= 2002,
    'iyr': lambda x: 2010 <= int(x) <= 2020,
    'eyr': lambda x: 2020 <= int(x) <= 2030,
    'hgt': lambda x: any((x.endswith('cm') and 150 <= int(x[:-2]) <= 193,
                          x.endswith('in') and 59 <= int(x[:-2]) <= 76)),
    'hcl': lambda x: re.match(r'^#\w{6}$', x),
    'ecl': lambda x: x in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'),
    'pid': lambda x: re.match(r'^\d{9}$', x)
    }


def parse_passports(raw_lines: List[str]) -> Iterable[Dict]:
    passport: Dict = {}
    for line in raw_lines:
        if not line:
            yield passport
            passport = {}
        else:
            new_fields = dict(pair.split(':') for pair in line.split())  # type: ignore
            passport.update(new_fields)
    if passport:
        yield passport


def contains_required_fields(entry: Dict) -> bool:
    return set(entry).issuperset(REQUIRED_FIELDS.keys())


def are_fields_valid(entry: Dict) -> bool:
    return all(validate(entry[key]) for key, validate in REQUIRED_FIELDS.items())


def part1(data: List[Dict]) -> int:
    return sum(contains_required_fields(entry) for entry in data)


def part2(data: List[Dict]) -> int:
    return sum(
        contains_required_fields(entry) and are_fields_valid(entry) for entry in data
    )


if __name__ == '__main__':
    parsed_data = list(parse_passports(get_file_lines()))

    print(part1(parsed_data))  # 228
    print(part2(parsed_data))  # 175
