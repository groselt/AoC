#! /usr/bin/env python3

from collections import defaultdict
import math
from typing import Dict, Iterable, List, Set

from utils import get_file_lines


TOP = 0
LEFT = 1
BOTTOM = 2
RIGHT = 3

class Tile:
    def __init__(self, id: int, data: List[str]):
        self.id = id
        self.data = data

    @property
    def top(self) -> str:
        return self.data[0]

    @property
    def bottom(self) -> str:
        return self.data[-1]

    @property
    def left(self) -> str:
        return self._get_column(0)

    @property
    def right(self) -> str:
        return self._get_column(len(self.data)-1)

    def can_connect(self, other: 'Tile') -> bool:
        other_orienations = other.generate_all_side_orienations()
        return self.left in other_orienations \
            or self.top in other_orienations \
                or self.right in other_orienations \
                    or self.bottom in other_orienations

    def _get_column(self, col: int) -> str:
        return ''.join(row[col] for row in self.data)

    def generate_all_side_orienations(self) -> Set[str]:
        return {
            self.top, self.top[::-1], 
            self.right, self.right[::-1],
            self.bottom, self.bottom[::-1],
            self.left, self.left[::-1]
        }

    def flip(self) -> None:
        for i, row in enumerate(self.data):
            self.data[i] = row[::-1]

    def rotate(self) -> None:
        data: List[str] = []
        for col in range(len(self.data[0])):
            data.append(self._get_column(col)[::-1])
        self.data = data


def parse_pieces(data: List[str]) -> Iterable[Tile]:
    current_id, current_data = None, []
    for line in data:
        if not line:
            yield Tile(current_id, current_data)
            current_id, current_data = None, []
        elif line.startswith('Tile'):
            current_id = int(line[5:-1])
        else:
            current_data.append(line)
    if current_data:
        yield Tile(current_id, current_data)


def get_column(data: List[str], col: int) -> str:
    return ''.join(row[col] for row in data)


def flip(data: List[str]) -> None:
    for i, row in enumerate(data):
        data[i] = row[::-1]


def rotated(data: List[str]) -> List[str]:
    new_data: List[str] = []
    for col in range(len(data[0])):
        new_data.append(get_column(data, col)[::-1])
    return new_data


def get_connections(tiles: Set[Tile]) -> Dict[int, List[int]]:
    connections: Dict[int, List[int]] = defaultdict(int)
    for tile in tiles:
        connections[tile.id] = []
        for other in tiles:
            if tile.id == other.id:
                continue
            if tile.can_connect(other):
                connections[tile.id].append(other.id)
    return connections
    

def orientate_top_left(id: int, tiles: Dict[int, Tile], connections: Dict[int, List[int]]) -> None:
    def all_neigbour_sides():
        sides = set()
        for neighbour in connections[id]:
            for side in tiles[neighbour].generate_all_side_orienations():
                sides.add(side)
        return sides

    def is_orientated(tile: Tile, other_sides: Set[str]):
        return tile.left not in other_sides and tile.top not in other_sides

    flips = 2
    rotations = 4
    tile = tiles[id]
    print(connections[id])
    for y in range(len(tile.data)):
        print(tile.data[y], '\t', tiles[connections[id][0]].data[y], '\t', tiles[connections[id][1]].data[y])
    print()
    other_sides = all_neigbour_sides()
    for _ in range(flips):
        for __ in range(rotations):
            print(tile.top)
            if is_orientated(tile, other_sides):
                return
            tile.rotate()
        print('flip')
        tile.flip()
    raise RuntimeError('Could not orientate top left tile')


def orientate_and_connect_left(left_side: str, tile: Tile) -> bool:
    flips = 2
    rotations = 4
    for _ in range(flips):
        for __ in range(rotations):
            if tile.left == left_side:
                return True
            tile.rotate()
        tile.flip()
    return False


def orientate_and_connect_top(top_side: str, tile: Tile) -> bool:
    flips = 2
    rotations = 4
    for _ in range(flips):
        for __ in range(rotations):
            if tile.top == top_side:
                return True
            tile.rotate()
        tile.flip()
    return False


def build_map(tiles: Dict[int, Tile], puzzle: List[List[int]]):
    result = []
    tile_row_count = len(list(tiles.values())[0].data)
    for row in range(len(puzzle)):
        for tile_row in range(1, tile_row_count-1):
            map_row = ''
            for col in range(len(puzzle[0])):
                tile = tiles[puzzle[row][col]]
                map_row += tile.data[tile_row][1:-1]
            result.append(map_row)
    return result


def get_mask_count(full_map: List[str], mask: List[str]) -> int:
    def mask_match(row, col):
        for mask_row in range(len(mask)):
            for mask_col in range(len(mask[0])):
                if mask[mask_row][mask_col] == '#' and \
                       full_map[row+mask_row][col+mask_col] != '#':
                    return False
        return True

    count = 0
    for row in range(len(full_map) - len(mask) + 1):
        for col in range(len(full_map[0]) - len(mask[0]) + 1):
            if mask_match(row, col):
                count += 1
    return count


def mark_mask(full_map: List[str], mask: List[str]):
    def mask_match(row, col):
        for mask_row in range(len(mask)):
            for mask_col in range(len(mask[0])):
                if mask[mask_row][mask_col] == '#' and \
                       full_map[row+mask_row][col+mask_col] != '#':
                    return False
        return True

    def mark(row, col):
        for mask_row in range(len(mask)):
            line = list(full_map[row+mask_row])
            for mask_col in range(len(mask[0])):
                if mask[mask_row][mask_col] == '#':
                    line[col+mask_col] = 'O'
                    # breakpoint()
            full_map[row+mask_row] = ''.join(line)

    for row in range(len(full_map) - len(mask) + 1):
        for col in range(len(full_map[0]) - len(mask[0]) + 1):
            if mask_match(row, col):
                mark(row, col)


def part1(tiles: Dict[int, Tile]) -> int:
    connections = get_connections(tiles.values())
    return math.prod(id for id, neighbours in connections.items() if len(neighbours) == 2)


def part2(tiles: Dict[int, Tile]) -> int:
    LEN = 12
    connections = get_connections(tiles.values())
    first_corner = next(id for id, neighbours in connections.items() if len(neighbours) == 2)
    orientate_top_left(first_corner, tiles, connections)
    puzzle = [[first_corner]]

    # Build first column
    last_id = first_corner
    for row in range(LEN-1):
        for bottom in connections[last_id]:
            if orientate_and_connect_top(tiles[last_id].bottom, tiles[bottom]):
                puzzle.append([bottom])
                last_id = bottom
                break

    # Build rows
    for row in range(LEN):
        left_id = puzzle[row][0]
        for col in range(LEN-1):
            for right in connections[left_id]:
                if orientate_and_connect_left(tiles[left_id].right, tiles[right]):
                    puzzle[row].append(right)
                    left_id = right

    full_map = build_map(tiles, puzzle)

    mask = ['                  # ',
            '#    ##    ##    ###',
            ' #  #  #  #  #  #   ']

    flips = 2
    rotations = 4
    map_orientations = dict()
    for _ in range(flips):
        for __ in range(rotations):
            print(full_map[0][:30])
            count = get_mask_count(full_map, mask)
            map_orientations[count] = full_map.copy()
            print(count)
            full_map = rotated(full_map)
        flip(full_map)

    max_monsters = max(map_orientations.keys())
    full_map = map_orientations[max_monsters]
    mark_mask(full_map, mask)
    for row in full_map:
        print(row)
    return sum(c == '#' for row in full_map for c in row)





if __name__ == '__main__':
    all_pieces = {piece.id: piece for piece in parse_pieces(get_file_lines())}

    # print(part1(all_pieces))  # 18449208814679
    print(part2(all_pieces))  # 1559
