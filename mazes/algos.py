import random
import time

import click

from mazes.maze import Generator


class Backtrack(Generator):
    """Randomly moves through the mazes until it hits a dead-end and backtracks to fill the maze."""

    name = "backtrack"

    def step(self):
        if len(self.stack) == 0:
            return None
        self.visit(self.current_cell.x, self.current_cell.y)
        choices = list(self.univisited_cells())
        if len(choices) == 0:
            self.backtrack()
            return self.step()
        choice = random.choice(choices)
        d = self.current_cell.direction(choice)
        self.current_cell.remove_wall(d)
        self.stack.append(choice)
        if self.config.show_updates:
            click.echo(self.maze.show())
            time.sleep(self.config.update_wait)
        return self.step()

    def backtrack(self):
        try:
            next(self.univisited_cells())
        except (IndexError, StopIteration):
            if len(self.stack) == 0:
                return
            self.stack.pop(-1)
            self.backtrack()
