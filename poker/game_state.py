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
        dealer_index: int = 0,
        sb_index: int = 0,
        bb_index: int = 0,
        small_blind: int = 0,
        big_blind: int = 0,
        current_bet: int = 0,
        bets: Optional[Dict[str, int]] = None,
        players_to_act: Optional[Set[str]] = None,
        last_raiser: Optional[str] = None,
        hand_number: int = 0,
        last_winner: Optional[str] = None,
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
        self.dealer_index = dealer_index
        self.sb_index = sb_index
        self.bb_index = bb_index
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.current_bet = current_bet
        self.bets = bets or {player: 0 for player in self.players_in_hand}
        self.players_to_act = players_to_act or set(self.players_in_hand)
        self.last_raiser = last_raiser
        self.hand_number = hand_number
        self.last_winner = last_winner

    def add_to_pot(self, amount: int) -> None:
        self.pot += amount

    def record_action(self, action: Action) -> None:
        self.action_history.append(action)

    def reset_betting_round(self) -> None:
        self.current_bet = 0
        self.bets = {player: 0 for player in self.players_in_hand}
        self.players_to_act = set(self.players_in_hand)
        self.last_raiser = None

    def to_call(self, player_id: str) -> int:
        return max(0, self.current_bet - self.bets.get(player_id, 0))

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
            f"dealer_index={self.dealer_index}, "
            f"sb_index={self.sb_index}, "
            f"bb_index={self.bb_index}, "
            f"current_bet={self.current_bet}, "
            f"bets={self.bets}, "
            f"action_history={self.action_history}, "
            f"players_in_hand={self.players_in_hand}, "
            f"hand_number={self.hand_number}, "
            f"last_winner={self.last_winner}"
            ")"
        )
