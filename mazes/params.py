import pathlib
import pickle

import click

from .store import MazeIO


class DimensionsParamType(click.ParamType):
    name = "dimensions"

    def convert(self, value, param, ctx):
        try:
            w, h = value.split("x")
            return int(w), int(h)
        except ValueError:
            return self.fail(f"{value!r} does not follow dimension scheme 'WxH'", param, ctx)


class MazeFileParamType(click.ParamType):
    name = "maze_file_path"

    def __init__(self, mazeio: MazeIO):
        self.mazeio = mazeio

    def convert(self, value, param, ctx):
        if pathlib.Path(value).is_file():
            value = pathlib.Path(value)
        elif pathlib.Path(self.mazeio.MAZES_DIRECTORY, value).is_file():
            value = pathlib.Path(self.mazeio.MAZES_DIRECTORY, value)
        else:
            return self.fail(f'The maze file "{value}" does not exist, sorry :(', param, ctx)
        with open(value, "rb") as f:
            maze = pickle.load(f)
            maze.location = value
            return maze


class ColorParamType(click.ParamType):
    name = "maze_file_path"

    def convert(self, value, param, ctx):
        colors = ["grey", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
        if value in colors:
            return value
        return self.fail(
            f"'{value}' is not a valid color. Valid colors are {', '.join(colors)}",
            param,
            ctx,
        )
