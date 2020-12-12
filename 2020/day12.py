#! /usr/bin/env python3

from itertools import chain
from typing import List, NamedTuple

from utils import get_file_lines


DIRECTION = {
    'N': complex(0, 1),
    'E' : complex(1, 0),
    'S': complex(0, -1),
    'W': complex(-1, 0)
    }

ROTATION_90 = {
    'L' : ((0, -1), (1, 0)),
    'R' : ((0, 1), (-1, 0))
}


class Instruction(NamedTuple):
    action: str
    parameter: int


class Navigation1:
    def __init__(self):
        self.position = complex(0, 0)
        self.facing = DIRECTION['E']

    def distance(self):
        return abs(self.position.real) + abs(self.position.imag)

    def apply(self, instruction: Instruction) -> None:
        if instruction.action == 'F':
            self.position += instruction.parameter * self.facing
        elif instruction.action in DIRECTION.keys():
            self.position += instruction.parameter * DIRECTION[instruction.action]
        else:
            self.rotate(ROTATION_90[instruction.action], instruction.parameter//90)

    def rotate(self, matrix, times: int):
        for _ in range(times % 4):
            self.facing = complex(
                            self.facing.real*matrix[0][0] + self.facing.imag*matrix[0][1],
                            self.facing.real*matrix[1][0] + self.facing.imag*matrix[1][1]
                            )


class Navigation2:
    def __init__(self, waypoint: complex):
        self.position = complex(0, 0)
        self.waypoint = waypoint

    def distance(self):
        return abs(self.position.real) + abs(self.position.imag)

    def apply(self, instruction: Instruction) -> None:
        if instruction.action == 'F':
            translation = instruction.parameter * (self.waypoint - self.position)
            self.position += translation
            self.waypoint += translation
        elif instruction.action in DIRECTION.keys():
            translation = instruction.parameter * DIRECTION[instruction.action]
            # self.position += translation
            self.waypoint += translation
        else:
            self.rotate(ROTATION_90[instruction.action], instruction.parameter//90)

    def rotate(self, matrix, times: int):
        for _ in range(times % 4):
            vector = self.waypoint - self.position
            self.waypoint = self.position + complex(
                            vector.real*matrix[0][0] + vector.imag*matrix[0][1],
                            vector.real*matrix[1][0] + vector.imag*matrix[1][1]
                            )


def parse_instruction(raw_instruction: str) -> Instruction:
    return Instruction(raw_instruction[0], int(raw_instruction[1:]))


def part1(instructions: List[Instruction]) -> int:
    navigation = Navigation1()
    for instruction in instructions:
        navigation.apply(instruction)
    return navigation.distance()


def part2(instructions: List[Instruction]) -> int:
    navigation = Navigation2(10+1j)
    for instruction in instructions:
        navigation.apply(instruction)
    return navigation.distance()


if __name__ == '__main__':
    all_instructions = [parse_instruction(instruction) for instruction in get_file_lines()]
    print(part1(all_instructions))  # 445
    print(part2(all_instructions))  # 42495
