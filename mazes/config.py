import typing as t
from dataclasses import dataclass


@dataclass()
class Config:
    algo: t.Optional[type] = None
    show_updates: bool = False
    update_wait: float = 1.0
