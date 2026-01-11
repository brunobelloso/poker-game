"""Game state container for the poker game."""

from __future__ import annotations

from typing import Dict, List, Optional, Set

from .actions import Action
from .cards import Card


class GameState:
    def __init__(
        self,
        players: List[str],
        stacks: Dict[str, int],
        pot: int = 0,
        board: Optional[List[Card]] = None,
        hands: Optional[Dict[str, List[Card]]] = None,
        current_player: Optional[str] = None,
        street: str = "preflop",
        action_history: Optional[List[Action]] = None,
        players_in_hand: Optional[Set[str]] = None,
        players_acted: Optional[Set[str]] = None,
    ) -> None:
        self.players = players
        self.stacks = stacks
        self.pot = pot
        self.board = board or []
        self.hands = hands or {}
        self.current_player = current_player
        self.street = street
        self.action_history = action_history or []
        self.players_in_hand = players_in_hand or set(players)
        self.players_acted = players_acted or set()

    def add_to_pot(self, amount: int) -> None:
        self.pot += amount

    def record_action(self, action: Action) -> None:
        self.action_history.append(action)

    def __repr__(self) -> str:
        return (
            "GameState("
            f"players={self.players}, "
            f"stacks={self.stacks}, "
            f"pot={self.pot}, "
            f"board={self.board}, "
            f"hands={self.hands}, "
            f"current_player={self.current_player}, "
            f"street={self.street}, "
            f"action_history={self.action_history}, "
            f"players_in_hand={self.players_in_hand}"
            ")"
        )
