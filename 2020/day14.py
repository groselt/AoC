#! /usr/bin/env python3

import re
from typing import Dict, Iterable, List, NamedTuple

from utils import get_file_lines


class Assignment(NamedTuple):
    address: int
    value: int


class Instruction(NamedTuple):
    mask: str
    settings: List[Assignment]


def to_bin(number: int, length: int = 36) -> str:
    return bin(number)[2:].rjust(length, '0')


def parse_instructions(lines: List[str]) -> List[Instruction]:
    result: List[Instruction] = []
    assign_pattern = re.compile(r'mem\[(\d+)\] = (\d+)')
    assignments = []
    for line in lines:
        if line.startswith('mask'):
            if assignments:
                result.append(Instruction(mask, assignments))
                assignments = []
            mask = line.split(' = ')[1]
        else:
            match = assign_pattern.match(line)
            assignments.append(Assignment(int(match.group(1)), int(match.group(2))))
    if assignments:
        result.append(Instruction(mask, assignments))
    return result


def part1(instructions: List[Instruction]) -> int:
    def apply_mask(mask: str, value: int) -> int:
        length = len(mask)
        bin_value = list(to_bin(value))
        assert length == len(bin_value)
        for i in range(length):
            if mask[i] != 'X':
                bin_value[i] = mask[i]
        return int(''.join(bin_value), 2)

    memory: Dict[int, int] = dict()  # {addr: value}
    for instruction in instructions:
        for setting in instruction.settings:
            memory[setting.address] = apply_mask(instruction.mask, setting.value)
    return sum(memory.values())


def part2(instructions: List[Instruction]) -> int:
    def all_addresses(address: int, mask: str) -> Iterable:
        float_count = mask.count('X')
        original_address = to_bin(address)
        for combination in range(2**float_count):
            subs = to_bin(combination, float_count)
            new_address = []
            combi_i = 0
            for i in range(len(mask)):
                if mask[i] == '0':
                    new_address.append(original_address[i])
                elif mask[i] == '1':
                    new_address.append('1')
                else:
                    new_address.append(subs[combi_i])
                    combi_i += 1
            yield int(''.join(new_address), 2)

    memory: Dict[int, int] = dict()  # {addr: value}
    for instruction in instructions:
        for setting in instruction.settings:
            for address in all_addresses(setting.address, instruction.mask):
                memory[address] = setting.value
    return sum(memory.values())


if __name__ == '__main__':
    raw_instructions = parse_instructions(get_file_lines())
    print(part1(raw_instructions))  # 10885823581193
    print(part2(raw_instructions))  # 3816594901962