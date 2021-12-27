#! /usr/bin/env python3.10

from collections import Counter, defaultdict

from utils import get_file_lines


def calc_population(timers: dict, days: int) -> int:
    for _ in range(days):
        next_gen = defaultdict(int)
        for timer, count in timers.items():
            if timer == 0:
                next_gen[8] = count
                next_gen[6] += count
            else:
                next_gen[timer-1] += count
        timers = next_gen
    return sum(timers.values())


def part1(timers: dict) -> int:
    return calc_population(timers, 80)


def part2(timers: list[int]) -> int:
    return calc_population(timers, 256)


if __name__ == '__main__':
    line = get_file_lines()[0]
    timers = Counter([int(i) for i in line.split(',')])
    print(part1(timers)) # 358214
    print(part2(timers)) # 1622533344325
