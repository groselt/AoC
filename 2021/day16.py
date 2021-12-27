#! /usr/bin/env python3.10

import math
from typing import Iterable, NamedTuple

from utils import get_raw_input


class Header(NamedTuple):
    version: int
    type_id: int


class Message:
    def __init__(self, header: Header):
        self.header =  header
    def sub_messages(self) -> Iterable:
        return []
    def value(self) -> int:
        raise NotImplementedError()


class Value(Message):
    def __init__(self, header: Header, value: int):
        super().__init__(header)
        self.constant = value
    def value(self) -> int:
        return self.constant


class Operator(Message):
    def __init__(self, header: Header, msgs: list[Message]):
        super().__init__(header)
        self.msgs = msgs
    def sub_messages(self) -> Iterable:
        return self.msgs
    def value(self) -> int:
        subs = self.sub_messages()
        match self.header.type_id:
            case 0: return sum(s.value() for s in subs)
            case 1: return math.prod(s.value() for s in subs)
            case 2: return min(s.value() for s in subs)
            case 3: return max(s.value() for s in subs)
            case 5: return 1 if subs[0].value() > subs[1].value() else 0
            case 6: return 1 if subs[0].value() < subs[1].value() else 0
            case 7: return 1 if subs[0].value() == subs[1].value() else 0
            case _: raise RuntimeError(f'Cannot handle type {self.header.type_id}') 


def hex2bin(line: str) -> str:
    def _char2bin(char: str) -> str:
        return bin(int(char, 16)).split('b')[1].rjust(4, '0')
    return ''.join(_char2bin(c) for c in line)


def bin2int(bits: str) -> int:
    return int(bits, 2)


def extract_header(bits: str) -> tuple[Header, str]:
    return Header(bin2int(bits[:3]), bin2int(bits[3:6])), bits[6:]


def decode_t4_value(body: str) -> tuple[int, int]:
    data = ''
    offset = 0
    last_read = False
    while not last_read:
        data += body[offset+1:offset+5]
        last_read = body[offset] == '0'
        offset += 5
    return bin2int(data), offset


def parse_message(bits: str) -> tuple[Message, str]:
    header, body = extract_header(bits)
    if header.type_id == 4:
        value, length = decode_t4_value(body)
        return Value(header, value), body[length:]
    else:
        length_type = body[0]
        if length_type == '0':
            body_length = bin2int(body[1:16])
            msgs = []
            msg_body = body[16:16+body_length]
            while msg_body:
                new_msg, msg_body = parse_message(msg_body)
                msgs.append(new_msg)
            return Operator(header, msgs), body[16+body_length:]
        else:
            sub_msg_count = bin2int(body[1:12])
            msgs = []
            msg_body = body[12:]
            for i in range(sub_msg_count):
                new_msg, msg_body = parse_message(msg_body)
                msgs.append(new_msg)
            return Operator(header, msgs), msg_body
    raise RuntimeError('Could not parse message')


def part1(bits: str) -> int:
    message, _ = parse_message(bits)
    stack = [message]
    versions = 0
    while stack:
        msg = stack.pop()
        versions += msg.header.version
        for child in msg.sub_messages():
            stack.append(child)
    return versions


def part2(bits: str) -> int:
    message, _ = parse_message(bits)
    return message.value()


if __name__ == '__main__':
    raw_input = get_raw_input()
    bits = hex2bin(raw_input)
    print(part1(bits)) # 904
    print(part2(bits)) # 200476472872
