#! /usr/bin/env python3.10

from collections import Counter, defaultdict
from itertools import chain, pairwise
from typing import Tuple

from utils import get_file_lines
Pins = set[str]
Signal = Tuple[Pins, Pins, Pins, Pins, Pins, Pins, Pins, Pins, Pins, Pins]
Output = Tuple[Pins, Pins, Pins, Pins]


def parse_lines(lines: list[str]) -> list[Tuple[Signal, Output]]:
    def _parse_line(line: str) -> Tuple[Signal, Output]:
        signal_line, output_line = line.split(' | ')
        signal_pins = [set(s) for s in signal_line.split()]
        output_pins = [set(s) for s in output_line.split()]
        return signal_pins, output_pins
    return [_parse_line(line) for line in lines]


def decode_signal(signal: Signal) -> list[set[str]]:
    one = [s for s in signal if len(s) == 2][0]
    four = [s for s in signal if len(s) == 4][0]
    seven = [s for s in signal if len(s) == 3][0]
    eight = [s for s in signal if len(s) == 7][0]

    _235 = [s for s in signal if len(s) == 5]
    _069 = [s for s in signal if len(s) == 6]

    two = _235[0] if _235[0] | four == eight else \
            _235[1] if _235[1] | four == eight else \
            _235[2]

    three = _235[0] if len(_235[0] & one) == 2 else \
            _235[1] if len(_235[1] & one) == 2 else \
            _235[2]

    five = [s for s in _235 if s not in [two, three]][0]

    six = _069[0] if _069[0] | one == eight else \
            _069[1] if _069[1] | one == eight else \
            _069[2]

    nine = _069[0] if len(_069[0] | three) == 6 else \
            _069[1] if len(_069[1] | three) == 6 else \
            _069[2]

    zero = [s for s in _069 if s not in [six, nine]][0]

    return [zero, one, two, three, four, five, six, seven, eight, nine]


def decode_output(signal: Signal, output: Output) -> int:
    digits = decode_signal(signal)
    return digits.index(set(output[0])) * 1000 \
            + digits.index(set(output[1])) * 100 \
            + digits.index(set(output[2])) * 10 \
            + digits.index(set(output[3]))


def part1(signal_output_list: list[Tuple[Signal, Output]]) -> int:
    known_lengths = {2, 4, 3, 7}
    return sum(1 
                for _, outputs in signal_output_list
                for o in outputs if len(o) in known_lengths)


def part2(signal_output_list: list[Tuple[Signal, Output]]) -> int:
    return sum(decode_output(signal, output) for signal, output in signal_output_list)

if __name__ == '__main__':
    lines = get_file_lines()
    signal_output_list = parse_lines(lines)
    print(part1(signal_output_list)) # 
    print(part2(signal_output_list)) # 915941
