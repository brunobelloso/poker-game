"""Base player definition."""

from poker.game_state import GameState


class BasePlayer:
    def __init__(self, player_id: str) -> None:
        self.id = player_id
        self.engine = None

    def decide(self, game_state: GameState):
        raise NotImplementedError
