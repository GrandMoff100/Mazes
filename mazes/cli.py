import click
import colorama
import pathlib
import pickle


from mazes import Maze
from mazes.store import MazeIO


class xDimensionsParamType(click.ParamType):
    name = "dimensions"

    def convert(self, value, param, ctx):
        try:
            w, h = value.split('x')
            return int(w), int(h)
        except ValueError:
            self.fail(f"{value!r} does not follow dimension scheme 'WxH'", param, ctx)


class MazeFileParamType(click.ParamType):
    name = "maze_file_path"

    def convert(self, value, param, ctx):
        if pathlib.Path(value).is_file():
            with open(value, 'rb') as f:
                return pickle.load(f)
        elif pathlib.Path(MAZE_STORE.MAZES_DIRECTORY, value).is_file():
            with open(pathlib.Path(MAZE_STORE.MAZES_DIRECTORY, value), 'rb') as f:
                return pickle.load(f)
        self.fail(f'The maze file "{value}" does not exist, sorry :(', param, ctx)


MAZE_FILE = MazeFileParamType()
DIMENSIONS = xDimensionsParamType()
MAZE_STORE = MazeIO()


@click.group()
def cli():
    """
    Makes and solves some mazes!!
    Mazes generated are saved in ~/.mazes
    """


@cli.command(name='generate')
@click.argument('dimensions', type=DIMENSIONS)
@click.option('-n', '--name')
@click.option('-s', '--show-creation', is_flag=True)
@click.option('--update-wait', type=float, default=1)
def cli_generate(dimensions: tuple, update_wait: int, name=None, show_creation=False):
    """Generates mazes using the recursive backtracker algorithm."""
    maze = Maze(*dimensions)
    maze.generate(show_updates=show_creation, update_wait=update_wait)
    print(colorama.ansi.clear_screen())
    name = MAZE_STORE.save_maze(maze, name)
    print('{}x{} maze saved as "{}"'.format(*dimensions, name))


@cli.command(name='solve')
def cli_solve():
    """Solves mazes that are generated."""


@cli.command('list')
def cli_list():
    """Lists the maze files that are saved in ~/.mazes"""
    print(MAZE_STORE.list_mazes())


@cli.command(name='show')
@click.argument('maze', type=MAZE_FILE)
def cli_show(maze):
    """Displays the maze content of maze files"""
    print(maze.show(3))


if __name__ == '__main__':
    cli()

