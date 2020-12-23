#! /usr/bin/env python3

from typing import List, Optional, Tuple

from utils import get_file_lines


class Node:  # pylint: disable=too-few-public-methods.
    def __init__(self, number: int):
        self.number = number
        self.next: Optional[Node] = None


def build_ring(numbers: List[int]) -> Node:
    first = Node(numbers[0])
    prev = first
    for number in numbers[1:]:
        next_node = Node(number)
        prev.next = next_node
        prev = next_node
    prev.next = first
    return first


def remove_after(node: Node, length: int) -> Node:
    removed_head = node.next
    current = removed_head
    for _ in range(1, length):
        removed_tail = current.next
        current = current.next
    node.next = removed_tail.next
    removed_tail.next = None
    return removed_head


def insert_section(head: Node, section_head: Node) -> None:
    section_tail = head.next
    head.next = section_head
    while head.next:
        head = head.next
    head.next = section_tail


def contains(head: Node, number: int) -> bool:
    while head:
        if head.number == number:
            return True
        head = head.next
    return False


def find_node(head: Node, label: int) -> Node:
    while head.number != label:
        head = head.next
    return head


def get_result1(head: Node) -> int:
    node_one = find_node(head, 1)
    current = node_one.next
    result = 0
    while current != node_one:
        result = result * 10 + current.number
        current = current.next
    return result


def print_cups(current: Node) -> None:
    print(f'({current.number})', end=' ')
    start: Optional[Node] = current
    while (current := current.next) != start:
        print(current.number, end=' ')
    print()


def part1(current: Node) -> int:
    for _ in range(100):
        removed = remove_after(current, 3)
        dest_label = current.number - 1
        if dest_label == 0:
            dest_label = 9
        while contains(removed, dest_label):
            dest_label -= 1
            if dest_label == 0:
                dest_label = 9
        dest_node = find_node(current, dest_label)
        insert_section(dest_node, removed)
        current = current.next

    return get_result1(current)


def part2(original: Tuple[int, ...]) -> int:
    size = 1_000_000
    ring = [0] * (size + 1)
    for i in range(len(original)-1):
        ring[original[i]] = original[i+1]
    ring[original[-1]] = 10
    for i in range(len (original)+1, size):
        ring[i] = i + 1
    ring[1_000_000] = original[0]

    current = original[0]
    removed = [0] * 3
    for _ in range(10_000_000):
        # remove
        removed[0] = ring[current]
        removed[1] = ring[removed[0]]
        removed[2] = ring[removed[1]]
        ring[current] = ring[removed[2]]

        # find destination
        destination = size if current == 1 else current - 1
        while destination in removed:
            destination = size if destination == 1 else destination - 1

        # insert
        ring[removed[2]] = ring[destination]
        ring[destination] = removed[0]

        # next
        current = ring[current]

    return ring[1] * ring[ring[1]]


if __name__ == '__main__':
    raw_data = [int(number) for number in list(get_file_lines()[0])]
    start_node = build_ring(raw_data)
    print(part1(start_node))  # 74698532
    print(part2(tuple(raw_data)))  # 286194102744
