#! /usr/bin/env python3

from collections import defaultdict
import math
from typing import Dict, Iterable, List, Callable, Set

from utils import get_file_lines

PUZZLE_WIDTH = 12
MAX_FLIPS = 2
MAX_ROTATIONS = 4

GetTileSide = Callable[['Tile'], str]
GetTileSide1 = Callable[['Tile'], str]

class Tile:
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    LEFT = 4

    def __init__(self, _id: int, data: List[str]):
        self.id = _id
        self.data = data

    @property
    def top(self) -> str:
        return self.data[0]

    @property
    def bottom(self) -> str:
        return self.data[-1]

    @property
    def left(self) -> str:
        return get_column(self.data, 0)

    @property
    def right(self) -> str:
        return get_column(self.data, len(self.data)-1)

    def get_side(self, direction: int) -> str:
        if direction == Tile.TOP:
            return self.top
        if direction == Tile.RIGHT:
            return self.right
        if direction == Tile.BOTTOM:
            return self.bottom
        if direction == Tile.LEFT:
            return self.left
        raise RuntimeError(f'Unhandled direction {direction}')


    def can_connect(self, other: 'Tile') -> bool:
        other_orienations = other.generate_all_side_orienations()
        return self.left in other_orienations \
            or self.top in other_orienations \
                or self.right in other_orienations \
                    or self.bottom in other_orienations

    def generate_all_side_orienations(self) -> Set[str]:
        return {
            self.top, self.top[::-1],
            self.right, self.right[::-1],
            self.bottom, self.bottom[::-1],
            self.left, self.left[::-1]
        }

    def flip(self) -> None:
        flip(self.data)

    def rotate(self) -> None:
        self.data = rotated(self.data)

    def orientate_and_connect(self, side: int, other_side: str) -> bool:
        for _ in self.get_all_orientations():
            if self.get_side(side) == other_side:
                return True
        return False

    def get_all_orientations(self) -> Iterable:
        for _ in range(MAX_FLIPS):
            for _ in range(MAX_ROTATIONS):
                yield self
                self.rotate()
            self.flip()


def parse_pieces(data: List[str]) -> Iterable[Tile]:
    current_id: int = -1
    current_data: List[str] = []
    for line in data:
        if not line:
            yield Tile(current_id, current_data)
            current_id, current_data = -1, []
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
    connections: Dict[int, List[int]] = defaultdict(list)
    for tile in tiles:
        connections[tile.id] = []
        for other in tiles:
            if tile.id == other.id:
                continue
            if tile.can_connect(other):
                connections[tile.id].append(other.id)
    return connections


def orientate_top_left(_id: int, tiles: Dict[int, Tile], connections: Dict[int, List[int]]) -> None:
    def all_neigbour_sides():
        sides = set()
        for neighbour in connections[_id]:
            for side in tiles[neighbour].generate_all_side_orienations():
                sides.add(side)
        return sides

    def is_orientated(tile: Tile, other_sides: Set[str]):
        return tile.left not in other_sides and tile.top not in other_sides

    tile = tiles[_id]
    other_sides = all_neigbour_sides()
    for _ in tile.get_all_orientations():
        if is_orientated(tile, other_sides):
            return
    raise RuntimeError('Could not orientate top left tile')


def build_map(tiles: Dict[int, Tile], puzzle: List[List[int]]):
    result = []
    tile_row_count = len(list(tiles.values())[0].data)
    for puzzle_row in puzzle:
        for tile_row in range(1, tile_row_count-1):
            map_row = ''
            for col in range(len(puzzle[0])):
                tile = tiles[puzzle_row[col]]
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


def get_all_map_orientations(data: List[str]) -> Iterable[List[str]]:
    for _ in range(MAX_FLIPS):
        for _ in range(MAX_ROTATIONS):
            yield data
            data = rotated(data)
        flip(data)


def part1(tiles: Dict[int, Tile]) -> int:
    connections = get_connections(set(tiles.values()))
    return math.prod(id for id, neighbours in connections.items() if len(neighbours) == 2)


def part2(tiles: Dict[int, Tile]) -> int:
    connections = get_connections(set(tiles.values()))
    first_corner = next(id for id, neighbours in connections.items() if len(neighbours) == 2)
    orientate_top_left(first_corner, tiles, connections)
    puzzle = [[first_corner]]

    # Build first column
    last_id = first_corner
    for row in range(PUZZLE_WIDTH-1):
        for bottom in connections[last_id]:
            if tiles[bottom].orientate_and_connect(Tile.TOP, tiles[last_id].bottom):
                puzzle.append([bottom])
                last_id = bottom
                break

    # Build rows
    for row in range(PUZZLE_WIDTH):
        left_id = puzzle[row][0]
        for _ in range(PUZZLE_WIDTH-1):
            for right in connections[left_id]:
                if tiles[right].orientate_and_connect(Tile.LEFT, tiles[left_id].right):
                    puzzle[row].append(right)
                    left_id = right

    full_map = build_map(tiles, puzzle)

    mask = ['                  # ',
            '#    ##    ##    ###',
            ' #  #  #  #  #  #   ']

    map_orientations = dict()
    for new_map in get_all_map_orientations(full_map):
        monster_count = get_mask_count(new_map, mask)
        map_orientations[monster_count] = new_map.copy()

    monster_count = max(map_orientations.keys())
    full_map = map_orientations[monster_count]
    mark_mask(full_map, mask)
    return sum(c == '#' for row in full_map for c in row)


if __name__ == '__main__':
    all_pieces = {piece.id: piece for piece in parse_pieces(get_file_lines())}

    print(part1(all_pieces))  # 18449208814679
    print(part2(all_pieces))  # 1559
