import random

import colorama
from termcolor import colored

from .config import Config

colorama.init()


class Point:
    def __init__(self, x, y, maze):
        self.maze = maze
        self.x = x
        self.y = y
        self.connections = self.adjacent_points()

    def __repr__(self):
        return "<Point {},{}>".format(self.x, self.y)

    def __lt__(self, point):
        return self._sortvalue() < point._sortvalue()

    def __le__(self, point):
        return self._sortvalue() <= point._sortvalue()

    def _sortvalue(self):
        return self.y * self.maze.width + self.x

    def collapse(self):
        self.connections = list(self.connections)

    def direction(self, point):
        if point.x == self.x:
            if point.y < self.y:
                return "u"
            if point.y > self.y:
                return "d"
        if point.y == self.y:
            if point.x < self.x:
                return "l"
            if point.x > self.x:
                return "r"
        return None

    def adjacent_points(self):
        if self.x > 0:
            yield self.maze.point(self.x - 1, self.y)
        if self.x < self.maze.width - 1:
            yield self.maze.point(self.x + 1, self.y)
        if self.y > 0:
            yield self.maze.point(self.x, self.y - 1)
        if self.y < self.maze.height - 1:
            yield self.maze.point(self.x, self.y + 1)

    def __eq__(self, point):
        return self.x == point.x and self.y == point.y

    def __ne__(self, point):
        return not self == point

    def is_connected(self, point):
        return point in self.connections

    def remove_connection(self, point):
        self.connections.remove(point)
        self.maze.point(point.x, point.y).connections.remove(self)


class Wall:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __eq__(self, wall):
        return sorted([self.p1, self.p2]) == sorted([wall.p1, wall.p2])

    def create(self):
        grid_p1 = self.p1.maze.point(self.p1.x, self.p1.y)
        grid_p2 = self.p2.maze.point(self.p2.x, self.p2.y)
        grid_p1.connections.append(grid_p2)
        grid_p2.connections.append(grid_p1)

    def remove(self):
        grid_p1 = self.p1.maze.point(self.p1.x, self.p1.y)
        grid_p2 = self.p2.maze.point(self.p2.x, self.p2.y)
        grid_p1.connections.remove(grid_p2)
        grid_p2.connections.remove(grid_p1)

    def edge_walls(self):
        m = self.p1.maze
        w, h = m.width, m.height
        for i in range(w - 1):
            for j in range(h - 1):
                yield Wall(m.point(i, 0), m.point(i + 1, 0))
                yield Wall(m.point(i, h - 1), m.point(i + 1, h - 1))
                yield Wall(m.point(0, j), m.point(0, j + 1))
                yield Wall(m.point(w - 1, j), m.point(w - 1, j + 1))


class Cell:
    def __init__(self, x, y, maze):
        self.x = x
        self.y = y
        self.maze = maze
        self.walls = {
            "u": Wall(self.maze.point(x, y), self.maze.point(x + 1, y)),
            "l": Wall(self.maze.point(x, y), self.maze.point(x, y + 1)),
            "r": Wall(self.maze.point(x + 1, y), self.maze.point(x + 1, y + 1)),
            "d": Wall(self.maze.point(x, y + 1), self.maze.point(x + 1, y + 1)),
        }

    def remove_wall(self, direction: str):
        self.walls[direction].remove()

    def add_wall(self, direction: str):
        self.walls[direction].create()

    def adjacent_cells(self):
        if self.x > 0:
            yield self.maze.cell(self.x - 1, self.y)
        if self.x < self.maze.width - 2:
            yield self.maze.cell(self.x + 1, self.y)
        if self.y > 0:
            yield self.maze.cell(self.x, self.y - 1)
        if self.y < self.maze.height - 2:
            yield self.maze.cell(self.x, self.y + 1)

    def direction(self, cell):
        if cell.x == self.x:
            if cell.y < self.y:
                return "u"
            if cell.y > self.y:
                return "d"
        if cell.y == self.y:
            if cell.x < self.x:
                return "l"
            if cell.x > self.x:
                return "r"
        return None


class Maze:
    """The maze grid class."""

    PLAYER_CHARACTER = "???"

    WALL_CHARACTERS = {
        "lr": "??????",
        "ld": "??????",
        "lu": "??????",
        "lrd": "??????",
        "lru": "??????",
        "ldu": "??????",
        "lrdu": "??????",
        "rd": "??????",
        "ru": "??????",
        "rdu": "??????",
        "du": "??????",
        "r": "??????",
        "l": "??????",
        "d": "??????",
        "u": "??????",
        "": "  ",
    }

    DIRECTION_ORDER = "lrdu"

    def __init__(self, width, height):
        self.width = width + 1
        self.height = height + 1

        self.grid = {
            j: {i: Point(i, j, self) for i in range(self.width)}
            for j in range(self.height)
        }
        self.collapse_cells()

        self.cells = {
            j: {i: Cell(i, j, self) for i in range(width)} for j in range(height)
        }

    def point(self, x, y):
        return self.grid[y][x]

    def cell(self, x, y):
        return self.cells[y][x]

    def collapse_cells(self):
        for i in range(self.width):
            for j in range(self.height):
                self.point(i, j).collapse()

    def show(self, bold=False, color=None, background=None):
        def horizontal_connectors():
            for j in range(self.height):
                for i in range(self.width):
                    p = self.point(i, j)
                    char = [p.direction(adj_p) for adj_p in p.connections]
                    yield self.WALL_CHARACTERS[
                        "".join(sorted(char, key=self.DIRECTION_ORDER.index))
                    ][int(bold)]
                    if p.is_connected(Point(i + 1, j, self)):
                        yield self.WALL_CHARACTERS["lr"][int(bold)] * 3
                    else:
                        if i < self.width - 1:
                            yield " " * 3
                yield "\n"

        def vertical_connectors():
            for j in range(self.height - 1):
                for i in range(self.width):
                    if self.point(i, j).is_connected(Point(i, j + 1, self)):
                        yield self.WALL_CHARACTERS["du"][int(bold)]
                    else:
                        yield " "
                    if i < self.width - 1:
                        yield " " * 3
                yield "\n"

        all_lines = "\n%s\n".join("".join(horizontal_connectors()).splitlines())
        in_between_lines = "".join(vertical_connectors()).splitlines()
        output = all_lines % tuple(in_between_lines)
        output = "\n".join(
            [
                colored(line, color=color, on_color=background)
                for line in output.splitlines()
            ]
        )
        return colorama.ansi.clear_screen() + output

    def generate(self, *args, **kwargs):
        gen = Generator(maze=self, *args, **kwargs)
        gen.step()
        gen.remove_start_to_end_walls()


class Generator:
    def __init__(self, maze: Maze, config: Config = Config(), start=None, end=None):
        self.maze = maze
        if start is None:
            start = 0, maze.height - 2
        if end is None:
            end = maze.width - 2, 0

        self.start = maze.cell(*start)
        self.end = maze.cell(*end)
        self.config = config

        self.visited = {
            j: {i: False for i in range(maze.width - 1)} for j in range(maze.height - 1)
        }
        self.stack = [self.start]
        self.morph_gen()

    def morph_gen(self) -> None:
        self.__class__ = self.config.algo  # pylint: disable=invalid-class-object
        # cls.__post_init__ ?

    @property
    def current_cell(self):
        return self.stack[-1]

    def visit(self, x, y):
        self.visited[y][x] = True

    def is_visited(self, x, y):
        return self.visited[y][x]

    def univisited_cells(self):
        for cell in self.current_cell.adjacent_cells():
            if not self.is_visited(cell.x, cell.y):
                yield cell

    def step(self):
        pass

    def remove_start_to_end_walls(self):
        def edge_cell_walls(cell):
            for wall in cell.walls.values():
                if wall in wall.edge_walls():
                    yield wall

        random.choice(list(edge_cell_walls(self.start))).remove()
        random.choice(list(edge_cell_walls(self.end))).remove()
