class Point:
    def __init__(self, x, y, maze):
        self.maze = maze
        self.x = x
        self.y = y
        self.connections = self.adjacent_points()
    
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
    
    def distance(self, point):
        return ((point.x - self.x)**2 + (point.y - self.y) ** 2)**0.5

    def adjacent_points(self):
        if self.x > 0:
            yield Point(self.x - 1, self.y, self.maze)
        if self.x < self.maze.width - 1:
            yield Point(self.x + 1, self.y, self.maze)
        if self.y > 0:
            yield Point(self.x, self.y - 1, self.maze)
        if self.y < self.maze.height - 1:
            yield Point(self.x, self.y + 1, self.maze)

    def __eq__(self, point):
        return self.x == point.x and self.y == point.y

    def is_connected(self, point):
        return self in list(point.adjacent_points())

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
    }

    DIRECTION_ORDER = 'lrdu'

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = {j:{i: Point(i, j, self) for i in range(width)} for j in range(height)}

    def point(self, x, y):
        return self.grid[y][x]
    
    def show(self, mx=1):
        def horizontal_connectors():
            for j in range(self.height):
                for i in range(self.width):
                    p = self.point(i, j)
                    char = [p.direction(adj_p) for adj_p in p.connections]
                    yield self.WALL_CHARACTERS[''.join(sorted(char, key=lambda x: self.DIRECTION_ORDER.index(x)))]
                    if Point(i + 1, j, self).is_connected(p):
                        yield self.WALL_CHARACTERS['lr'] * mx
                yield '\n'
        def vertical_connectors():
            for j in range(self.height - 1):
                for i in range(self.width):
                    if Point(i, j + 1, self).is_connected(self.point(i, j)):
                        yield self.WALL_CHARACTERS['du']
                    else:
                        yield ' '
                    yield ' ' * mx
                yield '\n'
        all_lines = '\n%s\n'.join(''.join(horizontal_connectors()).splitlines())
        in_between_lines = ''.join(vertical_connectors()).splitlines()
        return all_lines % tuple(in_between_lines)

m = Maze(10, 7)

print(m.show(3))

"""

"""
