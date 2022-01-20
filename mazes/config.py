from dataclasses import dataclass


@dataclass()
class Config:
    show_updates: bool = False
    update_wait: float = 1.0
