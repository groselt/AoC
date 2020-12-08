#! /usr/bin/env python3

from typing import Dict, List, NamedTuple, Tuple

from utils import get_file_lines


class Instruction(NamedTuple):
    operation: str
    param: int


class Computer:
    def __init__(self, program):
        self.instructions = self.parse(program)
        self.reset()

    @staticmethod
    def parse(program):
        instructions = []
        for line in program:
            words = line.split()
            instructions.append(Instruction(words[0], int(words[1])))
        return instructions

    def reset(self):
        self.ip = 0  # instruction pointer
        self.accumulator = 0

    def step(self):
        instruction = self.instructions[self.ip]
        if instruction.operation == 'nop':
            self.ip += 1
        elif instruction.operation == 'jmp':
            self.ip += instruction.param
        elif instruction.operation == 'acc':
            self.accumulator += instruction.param
            self.ip += 1
        else:
            raise RuntimeError(f'Unknown instruction {instruction.operation} at {self.ip}')


def run_to_loop_start(computer: Computer) -> bool:
    executed = set()
    while computer.ip not in executed and computer.ip < len(computer.instructions):
        executed.add(computer.ip)
        computer.step()
    return computer.ip < len(computer.instructions)


def part1(computer: Computer) -> int:
    assert run_to_loop_start(computer)
    return computer.accumulator


def part2(computer: Computer) -> int:
    def make_new_instruction(old: Instruction) -> Instruction:
        new_operation = 'jmp' if old.operation == 'nop' else 'nop'
        return Instruction(new_operation, old.param)

    for i in range(len(computer.instructions)):
        computer.reset()
        old_instruction = computer.instructions[i]
        if old_instruction.operation in ('jmp', 'nop'):
            computer.instructions[i] = make_new_instruction(old_instruction)
            if not run_to_loop_start(computer):
                return computer.accumulator
            computer.instructions[i] = old_instruction


if __name__ == '__main__':
    raw_instructions = get_file_lines()
    computer = Computer(raw_instructions)
    print(part1(computer))  # 2051
    print(part2(computer))  # 2304
