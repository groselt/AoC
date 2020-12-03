#! /usr/bin/env python3

from utils import get_raw_input


def part1(entries):
    for e in entries:
        other = 2020 - e
        if other in entries:
            print(e, other)
            return e * other


def part2(entries):
    for e1 in entries:
        for e2 in entries:
            if e1 == e2:
                continue
            other = 2020 - e1 - e2
            if other in entries:
                print(e1, e2, other)
                return e1 * e2 * other


if __name__ == '__main__':
    raw_input = [int(x) for x in get_raw_input().split()]
    entries = set(raw_input)
    print(part1(entries)) # 41979
    print(part2(entries)) # 193416912
