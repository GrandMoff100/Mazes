import sys
import os
import pathlib
import pickle


sys.setrecursionlimit(1000000)


class MazeIO:
    MAZES_DIRECTORY = pathlib.Path(
        os.environ.get(
            'MAZES_DIRECTORY',
            os.path.join(
                os.path.expanduser('~'),
                '.mazes'
            )
        )
    )

    def __init__(self):
        if not self.MAZES_DIRECTORY.is_dir():
            self.MAZES_DIRECTORY.mkdir()
    
    def list_mazes(self):
        return ' '.join([os.path.split(file)[1] for file in self.MAZES_DIRECTORY.iterdir()])
            
    def get_maze(self, file):
        with open(pathlib.Path(self.MAZES_DIRECTORY, file), 'rb') as f:
            return pickle.load(f)

    def delete_maze(self, file):
        try:
            os.remove(pathlib.Path(self.MAZES_DIRECTORY, file))
        except FileNotFoundError:
            print('File not found :(')

    def save_maze(self, maze, name=None):
        if name is None:
            name = self.next_unnamed()
        with open(pathlib.Path(self.MAZES_DIRECTORY, name), 'wb') as f:
            pickle.dump(maze, f)
        return name

    def next_unnamed(self):
        i = 0
        while f'unnamed-{i}.maze' in os.listdir(self.MAZES_DIRECTORY):
            i += 1
        return f'unnamed-{i}.maze'
