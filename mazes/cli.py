import click
import colorama

from mazes import Maze
from mazes.store import MazeIO

from .params import ColorParamType, DimensionsParamType, MazeFileParamType

MAZE_STORE = MazeIO()
MAZE_FILE = MazeFileParamType(MAZE_STORE)
DIMENSIONS = DimensionsParamType()
COLOR = ColorParamType()


@click.group()
def cli():
    """
    Makes and solves some mazes!!
    Mazes generated are saved in ~/.mazes
    """


@cli.command(name="generate")
@click.argument("dimensions", type=DIMENSIONS)
@click.option("-n", "--name")
@click.option("-s", "--show-creation", is_flag=True)
@click.option("--update-wait", type=float, default=1)
def cli_generate(dimensions: tuple, update_wait: int, name=None, show_creation=False):
    """Generates mazes using a recursive backtracker algorithm."""
    maze = Maze(*dimensions)
    maze.generate(show_updates=show_creation, update_wait=update_wait)
    click.echo(colorama.ansi.clear_screen())
    name = MAZE_STORE.save_maze(maze, name)
    click.echo('{}x{} maze saved as "{}"'.format(*dimensions, name))


@cli.command(name="delete")
@click.argument("maze", type=MAZE_FILE)
def cli_delete(maze):
    """Deletes maze files from your filesystem"""
    MAZE_STORE.delete_maze(maze.location)
    click.echo(f"Successfully removed {maze.location}")


@cli.command(name="solve")
def cli_solve():
    """Solves mazes that are generated."""


@cli.command("list")
def cli_list():
    """Lists the maze files that are saved in ~/.mazes"""
    click.echo(MAZE_STORE.list_mazes())


@cli.command(name="show")
@click.argument("maze", type=MAZE_FILE)
@click.option("--bold", is_flag=True)
@click.option("-c", "--color", type=COLOR, default=None)
@click.option("-b", "--background", type=COLOR, default=None)
def cli_show(maze, bold=False, color=None, background=None):
    """Displays the maze content of maze files"""
    if background:
        background = f"on_{background}"
    click.echo(maze.show(bold=bold, color=color, background=background))


if __name__ == "__main__":
    cli()
