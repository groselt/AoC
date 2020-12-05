#! /usr/bin/env python3

from typing import List

from utils import get_file_lines


def parse_ticket(raw_ticket: str) -> int:
    binary = raw_ticket.replace('F','0').replace('B','1').replace('L','0').replace('R','1')
    return int(binary, 2)


def part1(tickets: List[int]) -> int:
    return max(tickets)
    

def part2(tickets: List[int]) -> int:
    ticket_set = set(tickets)
    x = min(ticket_set) + 1
    i = 1
    while i <= len(tickets):
        if x not in ticket_set and \
            x-1 in ticket_set and \
            x+1 in ticket_set:
            return x
        x += 1
        i += 1
    return -1


if __name__ == '__main__':
    data = [parse_ticket(t) for t in get_file_lines()]
    print(part1(data))  # 911
    print(part2(data))  # 629
