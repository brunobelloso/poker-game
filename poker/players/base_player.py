"""Base player definition."""

from abc import ABC, abstractmethod

from poker.game_state import GameState


class BasePlayer(ABC):
    def __init__(self, player_id: int, name: str) -> None:
        self.player_id = player_id
        self.name = name

    @abstractmethod
    def decide(self, game_state: GameState):
        raise NotImplementedError
