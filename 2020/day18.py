#! /usr/bin/env python3

from typing import List, Tuple

from utils import get_file_lines


NUMBER = 0
OPERATOR = 1
SUB_EXPRESSION = 2
Token = Tuple[int, str, int]  # Type, Symbol, len

def first_token(line: str) -> Token:
    i = 0
    length = len(line)

    if line[i].isdigit():
        while i < length and line[i].isdigit():
            i += 1
        return (NUMBER, line[:i], i)

    if line[i] in ('+', '*'):
        return (OPERATOR, line[:i+1], 1)

    if line[i] == '(':
        brackets = 1
        while brackets != 0:
            i += 1
            if line[i] == '(':
                brackets += 1
            elif line[i] == ')':
                brackets -= 1
        return (SUB_EXPRESSION, line[1:i], i+2)

    raise RuntimeError(f'Unhandled line: {line}')


def calc(line: str) -> int:
    line = line.strip()

    token = first_token(line)
    if token[0] == NUMBER:
        left = int(token[1])
    elif token[0] == SUB_EXPRESSION:
        left = calc(token[1])
    else:
        raise RuntimeError(f'Unexpected token {token}')
    line = line[token[2]:].strip()

    while line:
        token = first_token(line)
        if token[0] != OPERATOR:
            raise RuntimeError(f'Operator expected; found {token}')
        operator = token[1]
        line = line[token[2]:].strip()

        token = first_token(line)
        if token[0] == NUMBER:
            right = int(token[1])
        elif token[0] == SUB_EXPRESSION:
            right = calc(token[1])
        else:
            raise RuntimeError(f'Unexpected token {token}')
        line = line[token[2]:].strip()

        if operator == '+':
            left += right
        elif operator == '*':
            left *= right
        else:
            raise RuntimeError(f'Unknown operator {operator}')

    return left


def find_brackets(line: str) -> Tuple[int, int]:
    end = line.index(')')
    start = end - 1
    while line[start] != '(':
        start -= 1
    return (start, end)


def left_number_start(line: str, end: int) -> int:
    start = end
    while not line[start].isdigit():
        start -= 1
    while start >= 0 and line[start].isdigit():
        start -= 1
    return start + 1


def right_number_end(line: str, start: int) -> int:
    end = start
    while not line[end].isdigit():
        end += 1
    while end < len(line) and line[end].isdigit():
        end += 1
    return end -1


def calc2(line: str) -> int:
    line = line.strip()
    print(line)

    while '(' in line:
        brackets = find_brackets(line)
        line = line[0:brackets[0]] \
               + str(calc2(line[brackets[0]+1:brackets[1]])) \
               + line[brackets[1]+1:]

    while '+' in line:
        pos = line.index('+')
        left_start = left_number_start(line, pos)
        right_end = right_number_end(line, pos)
        tot = int(line[left_start:pos]) + int(line[pos+1:right_end+1])
        line = line[:left_start] + str(tot) + line[right_end+1:]
        line = line.strip()
        print(line)

    while '*' in line:
        pos = line.index('*')
        left_start = left_number_start(line, pos)
        right_end = right_number_end(line, pos)
        print(f'{(line[left_start:pos])} * {line[pos+1:right_end+1]}')
        tot = int(line[left_start:pos]) * int(line[pos+1:right_end+1])
        line = line[:left_start] + str(tot) + line[right_end+1:]
        line = line.strip()
        print(line)

    return int(line)


def part1(lines: List[str]) -> int:
    return sum(calc(line) for line in lines)


def part2(lines: List[str]) -> int:
    return sum(calc2(line) for line in lines)


if __name__ == '__main__':
    raw_data = get_file_lines()
    print(part1(raw_data))  # 25190263477788
    print(part2(raw_data))  # 297139939002972
