#! /usr/bin/env python3

from typing import Callable, Iterable, List, NamedTuple

from utils import get_file_lines


Precedence = Callable[[str], int]

OPERAND = 1
OPERATOR = 2
OPEN_BRACKET = 3
CLOSE_BRACKET = 4

class Token(NamedTuple):
    ttype: int
    value: str


def tokenise(line: str) -> Iterable[Token]:
    line = line.strip()
    while line:
        ttype, length = None, 0
        if line[0] in ('+', '*'):
            ttype, length = OPERATOR, 1
        elif line[0] == '(':
            ttype, length = OPEN_BRACKET, 1
        elif line[0] == ')':
            ttype, length = CLOSE_BRACKET, 1
        elif line[0].isdigit():
            end = 1
            while end < len(line) and line[end].isdigit():
                end += 1
            ttype, length = OPERAND, end
        else:
            raise RuntimeError(f'Could not tokenise {line}')

        if ttype:
            token = Token(ttype, line[:length])
            line = line[length:].strip()
            yield token


def infix_to_postfix(line: str, precedence: Precedence) -> List[Token]:
    def is_stack_start():
        return not operator_stack or operator_stack[-1].value == '('
    result: List[Token] = []
    operator_stack: List[Token] = []
    for token in tokenise(line):
        if token.ttype == OPERAND:
            result.append(token)
        elif token.ttype == OPEN_BRACKET:
            operator_stack.append(token)
        elif token.ttype == CLOSE_BRACKET:
            while operator_stack[-1].ttype != OPEN_BRACKET:
                result.append(operator_stack.pop())
            operator_stack.pop()
        elif token.ttype == OPERATOR:
            this_prec = precedence(token.value)
            while not is_stack_start() and this_prec <= precedence(operator_stack[-1].value):
                result.append(operator_stack.pop())
            operator_stack.append(token)
    while operator_stack:
        result.append(operator_stack.pop())
    return result


def eval_postfix(tokens: List[Token]) -> int:
    ops = {
        '+': lambda x, y: x + y,
        '*': lambda x, y: x * y
    }
    stack: List[int] = []
    for token in tokens:
        if token.ttype == OPERAND:
            stack.append(int(token.value))
        elif token.ttype == OPERATOR:
            left = stack.pop()
            right = stack.pop()
            stack.append(ops[token.value](left, right))
    return stack.pop()


def part1(data: List[str]) -> int:
    def precedence(_: str) -> int:
        return 0
    postfix_list = [infix_to_postfix(line, precedence) for line in data]
    return sum(eval_postfix(line) for line in postfix_list)


def part2(data: List[str]) -> int:
    def precedence(operator: str) -> int:
        if operator == '+':
            return 2
        if operator == '*':
            return 1
        raise RuntimeError(f'Unhandled operator {operator}')
    postfix_list = [infix_to_postfix(line, precedence) for line in data]
    return sum(eval_postfix(line) for line in postfix_list)


if __name__ == '__main__':
    raw_data = get_file_lines()

    print(part1(raw_data))  # 25190263477788
    print(part2(raw_data))  # 297139939002972
