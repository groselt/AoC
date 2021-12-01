#! /usr/bin/env python3.10

from utils import get_file_lines


def count_increase(depths: list[int], lookback: int) -> int:
    count = 0
    for i in range(lookback, len(depths)):
        if depths[i] > depths[i-lookback]:
            count += 1
    return count


def part1(depths: list[int]) -> int:
    return count_increase(depths, 1)


def part2(depths: list[int]) -> int:
    return count_increase(depths, 3)


if __name__ == '__main__':
    depths = get_file_lines(transform=int)
    print(part1(depths)) # 1791
    print(part2(depths)) # 1822
