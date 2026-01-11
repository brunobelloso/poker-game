"""Poker engine interface."""

from typing import List, Optional

from .actions import Action, ActionType
from .deck import Deck
from .game_state import GameState
from .hand_evaluator import HAND_RANK_NAMES, evaluate_hand


class PokerEngine:
    def __init__(self, players: List[str], starting_stack: int) -> None:
        self.players = players
        self.starting_stack = starting_stack
        self.game_state: Optional[GameState] = None
        self.deck: Optional[Deck] = None
        self.current_player_index = 0
        self.showdown_winner: Optional[str] = None
        self.showdown_hand_rank: Optional[str] = None

    def start_hand(self) -> None:
        self.deck = Deck()
        self.deck.shuffle()

        hands = {player: self.deck.deal(2) for player in self.players}
        stacks = {player: self.starting_stack for player in self.players}

        self.game_state = GameState(
            players=self.players,
            stacks=stacks,
            pot=0,
            board=[],
            hands=hands,
            current_player=self.players[0],
            street="preflop",
            players_in_hand=set(self.players),
            players_acted=set(),
        )
        self.current_player_index = 0
        self.showdown_winner = None
        self.showdown_hand_rank = None

    def get_legal_actions(self, player_id: str) -> List[Action]:
        return [
            Action(ActionType.CHECK),
            Action(ActionType.CALL),
            Action(ActionType.RAISE),
            Action(ActionType.FOLD),
        ]

    def next_player(self) -> None:
        if self.game_state is None:
            raise RuntimeError("Hand has not been started.")

        if not self.game_state.players_in_hand:
            self.game_state.current_player = None
            return

        starting_index = self.current_player_index
        while True:
            self.current_player_index = (self.current_player_index + 1) % len(
                self.players
            )
            candidate = self.players[self.current_player_index]
            if candidate in self.game_state.players_in_hand:
                self.game_state.current_player = candidate
                return
            if self.current_player_index == starting_index:
                self.game_state.current_player = None
                return

    def apply_action(self, player_id: str, action: Action) -> None:
        if self.game_state is None:
            raise RuntimeError("Hand has not been started.")
        if self.deck is None:
            raise RuntimeError("Deck is not initialized.")

        self.game_state.record_action(action)
        if action.amount is not None:
            self.game_state.add_to_pot(action.amount)

        if action.action_type == ActionType.FOLD:
            self.game_state.players_in_hand.discard(player_id)

        self.game_state.players_acted.add(player_id)
        self.next_player()

        if self.game_state.players_in_hand.issubset(self.game_state.players_acted):
            self.advance_street()

    def advance_street(self) -> None:
        if self.game_state is None:
            raise RuntimeError("Hand has not been started.")
        if self.deck is None:
            raise RuntimeError("Deck is not initialized.")

        if self.game_state.street == "preflop":
            self.game_state.board.extend(self.deck.deal(3))
            self.game_state.street = "flop"
        elif self.game_state.street == "flop":
            self.game_state.board.append(self.deck.deal(1))
            self.game_state.street = "turn"
        elif self.game_state.street == "turn":
            self.game_state.board.append(self.deck.deal(1))
            self.game_state.street = "river"
        elif self.game_state.street == "river":
            self.game_state.street = "showdown"
            self.resolve_showdown()

        if self.game_state.street != "showdown":
            self.game_state.players_acted = set()
            self.current_player_index = -1
            self.next_player()

    def resolve_showdown(self) -> None:
        if self.game_state is None:
            raise RuntimeError("Hand has not been started.")

        results = {}
        for player in self.game_state.players_in_hand:
            player_cards = self.game_state.hands.get(player, [])
            combined = player_cards + self.game_state.board
            results[player] = evaluate_hand(combined)

        winner = max(results, key=results.get)
        winning_rank = HAND_RANK_NAMES[results[winner][0]]
        self.game_state.stacks[winner] += self.game_state.pot
        self.game_state.pot = 0
        self.showdown_winner = winner
        self.showdown_hand_rank = winning_rank
        print(f"Winner: {winner} with {winning_rank}")
