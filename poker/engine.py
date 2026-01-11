"""Poker engine interface."""

from typing import List

from .actions import Action
from .game_state import GameState


class PokerEngine:
    def __init__(self) -> None:
        self.game_state = GameState()

    def start_hand(self) -> None:
        raise NotImplementedError

    def get_legal_actions(self, player_id: int) -> List[Action]:
        raise NotImplementedError

    def apply_action(self, player_id: int, action: Action) -> None:
        raise NotImplementedError
