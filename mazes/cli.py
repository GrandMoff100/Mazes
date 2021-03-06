import click
import colorama

from mazes import Maze
from mazes.config import Config
from mazes.maze import Generator
from mazes.params import (
    AlgorithmParamType,
    ColorParamType,
    DimensionsParamType,
    MazeFileParamType,
)
from mazes.store import MazeIO

MAZE_STORE = MazeIO()
MAZE_FILE = MazeFileParamType(MAZE_STORE)
ALGORITHM = AlgorithmParamType()
DIMENSIONS = DimensionsParamType()
COLOR = ColorParamType()


@click.group()
def cli():
    """
    Makes and solves some mazes!!
    Mazes generated are saved in ~/.mazes
    """


@cli.command(name="generate")
@click.argument("dimensions", type=DIMENSIONS, envvar="MAZE_DIMENSIONS")
@click.option("-n", "--name")
@click.option("-s", "--show-creation", is_flag=True, envvar="SHOW_MAZE_CREATION")
@click.option("--update-wait", type=float, default=1, envvar="UPDATE_WAIT")
@click.option(
    "-a",
    "--algorithm",
    envvar="GENERATION_ALGORITHM",
    type=ALGORITHM,
    default="backtrack",
    help="The algorithm to generate a maze with. List available algoithms with `mazes algorithms`",
)
def cli_generate(
    dimensions: tuple, update_wait: int, algorithm: str, name=None, show_creation=True
):
    """Generates mazes using a recursive backtracker algorithm."""
    maze = Maze(*dimensions)
    maze.generate(
        config=Config(
            show_updates=show_creation, update_wait=update_wait, algo=algorithm
        )
    )
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


@cli.command("algorithms")
@click.argument("algorithm", type=ALGORITHM, required=False)
def cli_algorithms(algorithm):
    """List the algorithms available to generate and/or solve mazes with."""
    if algorithm is None:
        algos = [cls.name for cls in Generator.__subclasses__()]
        click.echo(" ".join(algos))
    else:
        click.echo(algorithm.__doc__)


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
