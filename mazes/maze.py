import random
import time
import colorama


colorama.init()


class Point:
    def __init__(self, x, y, maze):
        self.maze = maze
        self.x = x
        self.y = y
        self.connections = self.adjacent_points()
    
    def __repr__(self):
        return '<Point {},{}>'.format(self.x, self.y)

    def collapse(self):
        self.connections = list(self.connections)
    
    def direction(self, point):
        if point.x == self.x:
            if point.y < self.y:
                return 'u'
            if point.y > self.y:
                return 'd'
        if point.y == self.y:
            if point.x < self.x:
                return 'l'
            if point.x > self.x:
                return 'r'

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


class Cell:
    def __init__(self, x, y, maze):
        self.x = x
        self.y = y
        self.maze = maze
        self.walls = {
            'u': Wall(
                self.maze.point(x, y),
                self.maze.point(x + 1, y)
            ),
            'l': Wall(
                self.maze.point(x, y),
                self.maze.point(x, y + 1)
            ),
            'r': Wall(
                self.maze.point(x + 1, y),
                self.maze.point(x + 1, y + 1)
            ),
            'd': Wall(
                self.maze.point(x, y + 1),
                self.maze.point(x + 1, y + 1)
            )
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
                return 'u'
            if cell.y > self.y:
                return 'd'
        if cell.y == self.y:
            if cell.x < self.x:
                return 'l'
            if cell.x > self.x:
                return 'r'


class Maze:
    """The maze grid class."""

    PLAYER_CHARACTER = '■'

    WALL_CHARACTERS = {
        'lr': '─',
        'ld': '┐',
        'lu': '┘',
        'lrd': '┬',
        'lru': '┴',
        'ldu': '┤',
        'lrdu': '┼',
        'rd': '┌',
        'ru': '└',
        'rdu': '├',
        'du': '│',
        'r': '╶',
        'l': '╴',
        'd': '╷',
        'u': '╵',
        '': ' '
    }

    DIRECTION_ORDER = 'lrdu'

    def __init__(self, width, height):
        self.width = width + 1
        self.height = height + 1

        self.grid = {
            j:{
                i: Point(i, j, self) 
                for i in range(self.width)
            } for j in range(self.height)
        }
        self.collapse_cells()

        self.cells = {
            j:{
               i: Cell(i, j, self) for i in range(width) 
            } for j in range(height)
        }

    def point(self, x, y):
        return self.grid[y][x]
    
    def cell(self, x, y):
        return self.cells[y][x]
    
    def collapse_cells(self):
        for i in range(self.width):
            for j in range(self.height):
                self.point(i, j).collapse()

    def show(self, mx=1):
        def horizontal_connectors():
            for j in range(self.height):
                for i in range(self.width):
                    p = self.point(i, j)
                    char = [p.direction(adj_p) for adj_p in p.connections]
                    yield self.WALL_CHARACTERS[''.join(sorted(char, key=lambda x: self.DIRECTION_ORDER.index(x)))]
                    if p.is_connected(Point(i + 1, j, self)):
                        yield self.WALL_CHARACTERS['lr'] * mx
                    else:
                        yield ' ' * mx
                yield '\n'
        def vertical_connectors():
            for j in range(self.height - 1):
                for i in range(self.width):
                    if self.point(i, j).is_connected(Point(i, j + 1, self)):
                        yield self.WALL_CHARACTERS['du']
                    else:
                        yield ' '
                    if i < self.width - 1:
                        yield ' ' * mx
                yield '\n'
        all_lines = '\n%s\n'.join(''.join(horizontal_connectors()).splitlines())
        in_between_lines = ''.join(vertical_connectors()).splitlines()
        return colorama.ansi.clear_screen() + all_lines % tuple(in_between_lines)

    def generate(self, *args, **kwargs):
        gen = Generator(self, *args, **kwargs)
        gen.step()


class Generator:
    def __init__(self, maze: Maze, show_updates=False):
        self.maze = maze
        self.start = maze.cell(0, maze.height - 2)
        self.end = maze.cell(maze.width - 2, 0)
        self.show_updates = show_updates

        self.visited = {
            j: {
                i: False for i in range(maze.width - 1)
            } for j in range(maze.height - 1)
        }
        self.stack = [self.start]

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
        if len(self.stack) == 0:
            return
        self.visit(self.current_cell.x, self.current_cell.y)
        choices = list(self.univisited_cells())
        if len(choices) == 0:
            self.backtrack()
            return self.step()
        choice = random.choice(choices)
        d = self.current_cell.direction(choice)
        self.current_cell.remove_wall(d)
        self.stack.append(choice)
        if self.show_updates:
            print(self.maze.show(3))
            time.sleep(1)
        return self.step()

    def backtrack(self):
        try:
            next(self.univisited_cells())
        except (IndexError, StopIteration):
            if len(self.stack) == 0:
                return
            self.stack.pop(-1)
            self.backtrack()

