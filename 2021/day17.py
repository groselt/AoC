#! /usr/bin/env python3.10

import math
from typing import Iterable, NamedTuple, Optional

from utils import get_raw_input


class Target:
    def __init__(self, line: str):
        def parse_range(range: str) -> tuple[int, int]:
            return tuple(int(i) for i in range.split('..'))
        ranges = line[13:].split(', ')
        self.xmin, self.xmax = parse_range(ranges[0][2:])
        self.ymin, self.ymax = parse_range(ranges[1][2:])
    def contains(self, x: int, y: int):
        return self.xmin <= x <= self.xmax and self.ymin <= y <= self.ymax


def shoot(xspeed: int, yspeed: int, target: Target) -> bool:
    x, y = 0, 0
    while yspeed > 0 or y > target.ymin:
        x += xspeed
        y += yspeed
        if target.contains(x, y):
            return True
        if xspeed > 0:
            xspeed -= 1
        elif xspeed < 0:
            xspeed += 1
        yspeed -= 1
    return False


def find_all_velocities(target: Target) -> list[tuple[int,int]]:
    hits = []
    MAXX = max(abs(target.xmin), abs(target.xmax))
    MAXY = max(abs(target.ymin), abs(target.ymax))
    for x in range(-MAXX, MAXX + 1):
        for y in range(-MAXY, MAXY + 1):
            if shoot(x, y, target):
                hits.append((x, y))
    return hits


def part1(hits: list[tuple[int,int]]) -> int:
    maxyspeed = max(v[1] for v in hits)
    maxheight = maxyspeed * (maxyspeed+1) / 2
    return int(maxheight)


def part2(hits: list[tuple[int,int]]) -> int:
    return len(hits)


if __name__ == '__main__':
    raw_input = get_raw_input()
    target = Target(raw_input)
    # print(target.xmin, target.xmax, target.ymin, target.ymax)
    hits = find_all_velocities(target)
    print(part1(hits)) # 23005
    print(part2(hits)) # 2040
