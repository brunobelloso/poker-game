"""Human player implementation."""

from poker.game_state import GameState
from poker.players.base_player import BasePlayer


class HumanPlayer(BasePlayer):
    def decide(self, game_state: GameState):
        raise NotImplementedError
