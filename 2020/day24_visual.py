#! /usr/bin/env python3

from typing import Dict, List, Tuple

import graphics
import day24
from utils import get_file_lines


class Hexagon(graphics.Polygon):
    def __init__(self, x, y, length):
        delta_x =   (1, 0.5, -0.5, -1, -0.5, 0.5)
        delta_y = (0, -0.86602540378443864676372317075294, -0.86602540378443864676372317075294, 0, 0.86602540378443864676372317075294, -0.86602540378443864676372317075294)
        points = [(x, y)]
        for i in range(5):
            nx = points[-1][0] + length * delta_x[i]
            ny = points[-1][1] - length * delta_y[i]
            points.append((nx, ny))
        super().__init__([graphics.Point(i,j) for i,j in points])


class HexagonGrid:
    def __init__(self, left, top, col_count, row_count, length):
        self.cells = []
        self.filled_cells = set()
        y_length = length * 1.7320508075688772935274463415059
        for x in range(col_count):
            self.cells.append([])
            x_offset = left + 0.5 * length + 1.5 * length * x
            y_offset = top + (0 if x % 2 == 0 else y_length / 2)
            for y in range(row_count):
                hexagon = Hexagon(x_offset, y_offset + y * y_length, length)
                self.cells[-1].append(hexagon)

    def draw(self, graphwin):
        for row in self.cells:
            for cell in row:
                cell.draw(graphwin)

    def reset_cells(self, coords_to_fill):
        for coord in coords_to_fill:
            if coord not in self.filled_cells:
                y, x = int(coord.real), int(coord.imag)
                self.cells[y][x].setFill('red')
        for coord in (self.filled_cells - coords_to_fill):
            y, x = int(coord.real), int(coord.imag)
            self.cells[y][x].setFill('light grey')
        self.filled_cells = coords_to_fill


def get_grid_size(floors: List[Dict[complex, int]]) -> Tuple[int, int]:
    minx, miny, maxx, maxy = 0, 0, 0, 0
    for floor in floors:
        for pos in floor.keys():
            minx = min(minx, int(pos.real))
            miny = min(miny, int(pos.imag))
            maxx = max(maxx, int(pos.real))
            maxy = max(maxy, int(pos.imag))
    return (maxx-minx+3, maxy-miny+2)


def part1(floor: Dict[complex, int]) -> int:
    minx = int(min(pos.real for pos in floor.keys()))
    miny = int(min(pos.imag for pos in floor.keys()))
    maxx = int(max(pos.real for pos in floor.keys()))
    maxy = int(max(pos.imag for pos in floor.keys()))

    col_count, row_count = get_grid_size([floor])
    x_offset = (maxx - minx) // 2 + 1
    y_offset = (maxy - miny) // 2 

    win = graphics.GraphWin('Part 1', 1460, 920)
    grid = HexagonGrid(5, 5, col_count, row_count, 15)
    grid.draw(win)
    for pos, colour in floor.items():
        if colour:
            grid.cells[int(pos.real+x_offset)][int(pos.imag+y_offset)].setFill('red')
    win.getMouse()


def part2(floor: Dict[complex, int]) -> int:
    floors = [floor]
    for _ in range(20):
        floor = day24.next_floor(floor)
        floors.append(floor)

    col_count, row_count = get_grid_size(floors)
    x_offset = col_count // 2
    y_offset = row_count // 2
    center = complex(x_offset, y_offset)

    length = 10
    row_height = length*1.7320508075688772935274463415059
    print('cols',col_count, 'width',2*length*col_count + 10)
    win = graphics.GraphWin('Part 2', 1.5*length*col_count + 20, row_count*row_height + 20)
    grid = HexagonGrid(5, 5, col_count, row_count, length)
    grid.draw(win)
    for floor in floors:
        print(win.getMouse())
        grid.reset_cells(set([center+pos for pos in floor.keys()]))
    print(win.getMouse())

    return sum(floor.values())


if __name__ == '__main__':
    raw_data = get_file_lines('input/day24.txt')
    raw_floor = day24.get_initial_state(raw_data)
    part1(raw_floor)
    part2(raw_floor)
