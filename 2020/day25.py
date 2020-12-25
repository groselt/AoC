#! /usr/bin/env python3

from utils import get_file_lines


def get_loop_size(pubkey: int) -> int:
    value, size = 1, 0
    while value != pubkey:
        value = (value * 7) % 20201227
        size += 1
    return size


def calc_transform(pubkey: int, loop_size: int) -> int:
    value = 1
    for _ in range(loop_size):
        value = value * pubkey % 20201227
    return value


def part1(pubkey1: int, pubkey2: int) -> int:
    loopsize1 = get_loop_size(pubkey1)
    loopsize2 = get_loop_size(pubkey2)
    access1 = calc_transform(pubkey2, loopsize1)
    access2 = calc_transform(pubkey1, loopsize2)
    assert access1 == access2
    return access1


if __name__ == '__main__':
    raw_data = get_file_lines()
    raw_pubkey1, raw_pubkey2 = map(int, raw_data)
    print(part1(raw_pubkey1, raw_pubkey2))  # 18329280
