#! /usr/bin/env python3

from typing import Optional, Set

from utils import get_file_lines


def parse_ticket(raw_ticket: str) -> int:
    table = str.maketrans('FBLR', '0101')
    binary = raw_ticket.translate(table)
    return int(binary, 2)


def part1(tickets: Set[int]) -> int:
    return max(tickets)
    

def part2(tickets: Set[int]) -> Optional[int]:
    def is_gap(x: int) -> bool:
        return x not in tickets and \
            x-1 in tickets and \
            x+1 in tickets

    for x in range(min(tickets)+1, max(tickets)):
        if is_gap(x):
            return x
    return None


if __name__ == '__main__':
    data = set(parse_ticket(t) for t in get_file_lines())
    print(part1(data))  # 911
    print(part2(data))  # 629
