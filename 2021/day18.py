#! /usr/bin/env python3.10

from copy import deepcopy
from itertools import permutations
import math
from typing import Optional
from utils import get_file_lines


class Number:
    def magnitude(self) -> int:
        raise NotImplementedError()


class Regular(Number):
    def __init__(self, value: int):
        self.value = value
    def __str__(self) -> str:
        return str(self.value)
    def magnitude(self) -> int:
        return self.value


class Pair(Number):
    def __init__(self, left: Number, right: Number):
        self.left = left
        self.right = right
    def __str__(self) -> str:
        return f'[{self.left},{self.right}]'
    def magnitude(self) -> int:
        return 3*self.left.magnitude() + 2*self.right.magnitude()


def parse_line(line: str) -> Pair:
    stack = []
    for c in line:
        if c.isdigit():
            stack.append(Regular(int(c)))
        elif c == ']':
            right = stack.pop()
            left = stack.pop()
            stack.append(Pair(left, right))
    assert len(stack) == 1
    return stack.pop()


def first_left(pair: Pair, parents: list[Number]) -> Optional[Pair]:
    # left subtree to search
    candidate_roots = []
    for parent in reversed(parents):
        if parent.right in parents+[pair]:
            candidate_roots.append(parent.left)
    # right mmost value
    stack = list(reversed(candidate_roots))
    while stack:
        number = stack.pop()
        if isinstance(number, Regular):
            return number
        stack.append(number.left)
        stack.append(number.right)
    return None


def first_right(pair: Pair, parents: list[Number]) -> Optional[Pair]:
    # right subtree to search
    candidate_roots = []
    for parent in reversed(parents):
        if parent.left in parents+[pair]:
            candidate_roots.append(parent.right)
    # left mmost value
    stack = list(reversed(candidate_roots))
    while stack:
        number = stack.pop()
        if isinstance(number, Regular):
            return number
        stack.append(number.right)
        stack.append(number.left)
    return None


def apply_explosion(pair: Pair, parents: list[Number]) -> None:
        if parents[-1].left == pair:
            if (left := first_left(pair, parents)):
                left.value += pair.left.value
            if (right := first_right(pair, parents)):
                right.value += pair.right.value
            parents[-1].left = Regular(0)
        elif parents[-1].right == pair:
            if (right := first_right(pair, parents)):
                right.value += pair.right.value
            if (left := first_left(pair, parents)):
                left.value += pair.left.value
            parents[-1].right = Regular(0)
        else:
            raise RuntimeError()


def explode(pair: Pair, parents: list[Number]) -> bool:
    if len(parents) == 4:
        apply_explosion(pair, parents)
        return True
    else:
        if isinstance(pair.left, Pair) and explode(pair.left, parents + [pair]):
            return True
        return isinstance(pair.right, Pair) and explode(pair.right, parents + [pair])


def apply_split(number: Regular, parent: Pair) -> None:
    mid = number.value / 2
    new_pair = Pair(Regular(math.floor(mid)), Regular(math.ceil(mid)))
    if parent.left == number:
        parent.left = new_pair
    elif parent.right == number:
        parent.right = new_pair
    else:
        raise RuntimeError()


def split(pair: Pair) -> bool:
    stack = [(pair, None)]
    while stack:
        current, parent = stack.pop()
        if isinstance(current, Regular) and current.value > 9:
            apply_split(current, parent)
            return True
        elif isinstance(current, Pair):
            stack.extend([(current.right, current), (current.left, current)])
    return False


def reduce(pair: Pair) -> None:
    while True:
        if not explode(pair, []) and not split(pair):
            return


def part1(numbers: list[Pair]) -> int:
    total = numbers[0]
    for n in numbers[1:]:
        total = deepcopy(Pair(total, n))
        reduce(total)
    return total.magnitude()


def part2(numbers: list[Pair]) -> int:
    def score(a: Number, b: Number) -> int:
        total = Pair(deepcopy(a), deepcopy(b))
        reduce(total)
        return total.magnitude()
    return max(score(a, b) for a, b in permutations(numbers, 2))


if __name__ == '__main__':
    lines = get_file_lines()
    numbers = [parse_line(line) for line in lines]
    print(part1(numbers)) # 4120
    print(part2(numbers)) # 4725
