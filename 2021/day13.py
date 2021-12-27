#! /usr/bin/env python3.10

from typing import NamedTuple, Tuple

from utils import get_file_lines


Dots = dict[complex, bool]

class Fold(NamedTuple):
    axis: str
    position: int


def parse_lines(lines: list[str]) -> Tuple[Dots, list[Fold]]:
    dots, folds = dict(), list()
    i = 0
    while (line := lines[i]):
        i += 1
        x, y = [int(c) for c in line.split(',')]
        dots[complex(x, y)] = True

    # e.g. `fold along x=655`
    for line in lines[i+1:]:
        axis, position = line[11:].split('=')
        folds.append(Fold(axis, int(position)))

    return dots, folds


def print_dots(dots: dict[complex]) -> None:
    MAXX = max(int(c.real) for c in dots.keys()) + 1
    MAXY = max(int(c.imag) for c in dots.keys()) + 1
    for y in range(MAXY):
        for x in range(MAXX):
            print('#' if complex(x, y) in dots else '.', end='')
        print()


def apply_fold(dots: dict[complex], fold: Fold) -> None:
    to_add = dict()
    to_remove = []
    if fold.axis == 'x':
        for k in dots.keys():
            if k.real > fold.position:
                new_x = fold.position - (k.real - fold.position)
                to_add[complex(new_x, k.imag)] = True
                to_remove.append(k)
    elif fold.axis == 'y':
        for k in dots.keys():
            if k.imag > fold.position:
                new_y = fold.position - (k.imag - fold.position)
                to_add[complex(k.real, new_y)] = True
                to_remove.append(k)
    else:
        raise Exception(f'Unknown axis {fold.axis}')

    for dot in to_remove:
        dots.pop(dot)
    dots |= to_add

def part1(dots: list[list[int]], folds: list[Fold]) -> int:
    apply_fold(dots, folds[0])
    return len(dots)


def part2(dots: list[list[int]], folds: list[Fold]) -> None:
    for fold in folds[1:]:
        apply_fold(dots, fold)

if __name__ == '__main__':
    lines = get_file_lines()
    dots, folds = parse_lines(lines)
    print(part1(dots, folds)) # 827
    part2(dots, folds)
    print_dots(dots) # EAHKRECP
