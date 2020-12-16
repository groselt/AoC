#! /usr/bin/env python3

from collections import defaultdict
from typing import Dict, List, Optional, Tuple

from utils import get_raw_input


class Field:
    def __init__(self, rule: str) -> None:
        parts = rule.split(': ')
        ranges = parts[1].split(' or ')
        self.name = parts[0]
        self.range1: Tuple[int, int] = tuple(map(int, ranges[0].split('-')))  # type: ignore
        self.range2: Tuple[int, int] = tuple(map(int, ranges[1].split('-')))  # type: ignore

    def Contains(self, number: int) -> bool:
        return self.is_in_range(self.range1, number) or self.is_in_range(self.range2, number)

    @staticmethod
    def is_in_range(range: Tuple[int, int], number: int) -> bool:
        return range[0] <= number <= range[1]


def parse_raw_data(data: str) -> Tuple[List[Field], List[int], List[List[int]]]:
    parts = data.split('your ticket:')
    field_lines = parts[0].strip().split('\n')
    fields = [Field(line) for line in field_lines]
    ticket_parts = parts[1].split('nearby tickets:')
    my_ticket = list(map(int, ticket_parts[0].strip().split(',')))
    other_tickets = [list(map(int, line.split(','))) for line in ticket_parts[1].strip().split('\n')]
    assert len(fields) == len(my_ticket)
    for t in other_tickets:
        assert len(fields) == len(t)
    return fields, my_ticket, other_tickets


def get_invalid_number(fields: List[Field], ticket: List[int]) -> Optional[int]:
    for number in ticket:
        if not any(field.Contains(number) for field in fields):
            return number
    return None


def part1(fields: List[Field], tickets: List[List[int]]) -> int:
    total = 0
    for ticket in tickets:
        if (invalid_number := get_invalid_number(fields, ticket)) is not None:
            total += invalid_number  # type: ignore
    return total


def part2(fields: List[Field], my_ticket: List[int], other_tickets: List[List[int]]) -> int:
    valid_tickets = [ticket for ticket in other_tickets if get_invalid_number(fields, ticket) is None]
    candidates: Dict[str, List[int]] = defaultdict(list)
    for field in fields:
        for index in range(len(fields)):
            if all(field.Contains(t[index]) for t in valid_tickets):
                candidates[field.name].append(index)
    assignments: Dict[str, int] = dict()
    for candidate in sorted(candidates.items(), key=lambda x: len(x[1])):
        for index in candidate[1]:
            if index not in assignments.values():
                assignments[candidate[0]] = index
    result = 1
    for name, index in assignments.items():
        if name.startswith('departure'):
            result *= my_ticket[index]
    return result




if __name__ == '__main__':
    raw_data = get_raw_input()
    raw_fields, my_ticket, other_tickets = parse_raw_data(raw_data)
    print(part1(raw_fields, other_tickets))  # 29019
    print(part2(raw_fields, my_ticket, other_tickets))  # 517827547723
