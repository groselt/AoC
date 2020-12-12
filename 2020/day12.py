#! /usr/bin/env python3

from typing import List, NamedTuple, Tuple

from utils import get_file_lines


Matrix2D = Tuple[Tuple[int, int], Tuple[int, int]]

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


class Navigation:
    def __init__(self, waypoint: complex, loose_waypoint: bool):
        '''If `loose_waypoint` is True, position won't change
           when wind direction command is received'''
        self.position = complex(0, 0)
        self.waypoint = waypoint
        self.loose_waypoint = loose_waypoint

    def distance(self) -> int:
        return int(abs(self.position.real) + abs(self.position.imag))

    def apply(self, instruction: Instruction) -> None:
        if instruction.action == 'F':
            translation = instruction.parameter * (self.waypoint - self.position)
            self.position += translation
            self.waypoint += translation
        elif instruction.action in ROTATION_90.keys():
            self.rotate(ROTATION_90[instruction.action], instruction.parameter//90)
        else:
            wind_direction_change = instruction.parameter * DIRECTION[instruction.action]
            self.waypoint += wind_direction_change
            if not self.loose_waypoint:
                self.position += wind_direction_change

    def rotate(self, matrix: Matrix2D, times: int):
        for _ in range(times % 4):
            vector = self.waypoint - self.position
            self.waypoint = self.position + complex(
                            vector.real*matrix[0][0] + vector.imag*matrix[0][1],
                            vector.real*matrix[1][0] + vector.imag*matrix[1][1]
                            )


def parse_instruction(raw_instruction: str) -> Instruction:
    return Instruction(raw_instruction[0], int(raw_instruction[1:]))


def part1(instructions: List[Instruction]) -> int:
    navigation = Navigation(DIRECTION['E'], loose_waypoint=False)
    for instruction in instructions:
        navigation.apply(instruction)
    return navigation.distance()


def part2(instructions: List[Instruction]) -> int:
    navigation = Navigation(10+1j, loose_waypoint=True)
    for instruction in instructions:
        navigation.apply(instruction)
    return navigation.distance()


if __name__ == '__main__':
    all_instructions = [parse_instruction(instruction) for instruction in get_file_lines()]
    print(part1(all_instructions))  # 445
    print(part2(all_instructions))  # 42495
