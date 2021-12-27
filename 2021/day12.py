#! /usr/bin/env python3.10

from collections import defaultdict
from typing import NamedTuple

from utils import get_file_lines


class Vertex(NamedTuple):
    route: tuple[str]
    has_duplicate: bool


def build_graph(lines: list[str]) -> dict:
    graph = defaultdict(list)
    for line in lines:
        v1, v2 = line.split('-')
        graph[v1].append(v2)
        graph[v2].append(v1)
    return graph


def part1(graph: dict) -> int:
    unique_paths = set()
    stack = [('start',)]
    while stack:
        route = stack.pop()
        current = route[-1]
        if current == 'end':
            unique_paths.add(route)
            continue
        for to_vertex in graph[current]:
            if not to_vertex.islower() or to_vertex not in route:
                stack.append(route + (to_vertex,))
    return len(unique_paths)


def part2(graph: dict) -> int:
    unique_paths = set()
    stack = [Vertex(('start',), False),]  # route, has duplicate small cave
    while stack:
        route, has_duplicate = stack.pop()
        current = route[-1]
        if current == 'end':
            unique_paths.add(route)
            continue
        for to_vertex in graph[current]:
            if to_vertex != 'start' and (not to_vertex.islower()
                or to_vertex not in route or not has_duplicate):
                new_duplicate = has_duplicate or (to_vertex.islower() and to_vertex in route)
                new_route = route + (to_vertex,)
                stack.append(Vertex(new_route, new_duplicate))
    return len(unique_paths)


if __name__ == '__main__':
    lines = get_file_lines()
    graph = build_graph(lines)
    print(part1(graph)) # 3421
    print(part2(graph)) # 84870
