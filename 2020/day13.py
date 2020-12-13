#! /usr/bin/env python3

from typing import List, NamedTuple

from utils import get_file_lines


class RankedBus(NamedTuple):
    rank: int
    bus: int

def wait_time(now: int, bus_nr: int) -> int:
    return bus_nr - now % bus_nr


def part1(now: int, buses: List[int]) -> int:
    wait_to_bus = { wait_time(now, bus): bus for bus in buses }
    shortest_wait = min(wait_to_bus.keys())
    return shortest_wait * wait_to_bus[shortest_wait]


def part2(buses: List[RankedBus]) -> int:
    timestamp = 0
    period = buses[0][1]
    for bus in buses[1:]:
        offset = bus[0] % bus[1]
        while wait_time(timestamp, bus[1]) != offset:
            timestamp += period
        period *= bus[1]
    return timestamp


if __name__ == '__main__':
    all_lines = get_file_lines()
    start_time = int(all_lines[0])

    active_buses = [int(t) for t in all_lines[1].split(',') if t != 'x']
    print(part1(start_time, active_buses))  # 3997

    ranked_buses = [RankedBus(i, int(b)) for i, b in enumerate(all_lines[1].split(',')) if b != 'x']
    print(part2(ranked_buses))  # 500033211739354
