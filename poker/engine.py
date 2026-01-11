"""Poker engine interface."""

from typing import List, Optional

from .actions import Action, ActionType
from .deck import Deck
from .game_state import GameState
from .hand_evaluator import HAND_RANK_NAMES, evaluate_hand


class PokerEngine:
    def __init__(
        self,
        players: List[str],
        starting_stack: int,
        small_blind: int = 5,
        big_blind: int = 10,
    ) -> None:
        self.players = players
        self.starting_stack = starting_stack
        self.game_state: Optional[GameState] = None
        self.deck: Optional[Deck] = None
        self.current_player_index = 0
        self.showdown_winner: Optional[str] = None
        self.showdown_hand_rank: Optional[str] = None
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.dealer_index = 0

    def start_hand(self) -> None:
        self.deck = Deck()
        self.deck.shuffle()

        hands = {player: self.deck.deal(2) for player in self.players}
        if self.game_state is None:
            stacks = {player: self.starting_stack for player in self.players}
            hand_number = 0
        else:
            stacks = self.game_state.stacks
            hand_number = self.game_state.hand_number

        self.game_state = GameState(
            players=self.players,
            stacks=stacks,
            pot=0,
            board=[],
            hands=hands,
            current_player=None,
            street="preflop",
            players_in_hand=set(self.players),
            players_acted=set(),
            dealer_index=self.dealer_index,
            small_blind=self.small_blind,
            big_blind=self.big_blind,
            hand_number=hand_number,
            last_winner=None,
        )
        self._post_blinds()
        self.showdown_winner = None
        self.showdown_hand_rank = None

    def get_legal_actions(self, player_id: str) -> List[ActionType]:
        if self.game_state is None:
            raise RuntimeError("Hand has not been started.")
        if player_id not in self.game_state.players_in_hand:
            return []
        call_amt = self.game_state.to_call(player_id)
        if call_amt == 0:
            return [ActionType.CHECK, ActionType.RAISE, ActionType.FOLD]
        return [ActionType.CALL, ActionType.RAISE, ActionType.FOLD]

    def next_player(self) -> None:
        if self.game_state is None:
            raise RuntimeError("Hand has not been started.")

        if not self.game_state.players_in_hand:
            self.game_state.current_player = None
            return

        next_index = self._next_active_index(self.current_player_index)
        if next_index is None:
            self.game_state.current_player = None
            return
        self.current_player_index = next_index
        self.game_state.current_player = self.players[self.current_player_index]

    def apply_action(self, player_id: str, action: Action) -> None:
        if self.game_state is None:
            raise RuntimeError("Hand has not been started.")
        if self.deck is None:
            raise RuntimeError("Deck is not initialized.")
        if player_id != self.game_state.current_player:
            raise ValueError("It is not this player's turn.")
        if player_id not in self.game_state.players_in_hand:
            raise ValueError("Player is not in the hand.")

        call_amt = self.game_state.to_call(player_id)

        if action.type == ActionType.FOLD:
            self.game_state.record_action(action)
            self.game_state.players_in_hand.discard(player_id)
            self.game_state.players_to_act.discard(player_id)
            if len(self.game_state.players_in_hand) == 1:
                winner = next(iter(self.game_state.players_in_hand))
                self.showdown_hand_rank = "Uncontested"
                self.end_hand(winner)
                return
        elif action.type == ActionType.CHECK:
            if call_amt != 0:
                raise ValueError("Cannot check when facing a bet.")
            self.game_state.record_action(action)
            self.game_state.players_to_act.discard(player_id)
        elif action.type == ActionType.CALL:
            if call_amt <= 0:
                raise ValueError("Nothing to call.")
            contribution = min(self.game_state.stacks[player_id], call_amt)
            self.game_state.stacks[player_id] -= contribution
            self.game_state.bets[player_id] += contribution
            self.game_state.add_to_pot(contribution)
            self.game_state.record_action(action)
            self.game_state.players_to_act.discard(player_id)
        elif action.type == ActionType.RAISE:
            if action.amount is None:
                raise ValueError("Raise requires a target amount.")
            raise_to = action.amount
            if raise_to <= self.game_state.current_bet:
                raise ValueError("Raise must increase the current bet.")
            if raise_to - self.game_state.current_bet < self.game_state.big_blind:
                raise ValueError("Raise must meet the minimum raise size.")
            needed = raise_to - self.game_state.bets[player_id]
            contribution = min(self.game_state.stacks[player_id], needed)
            self.game_state.stacks[player_id] -= contribution
            self.game_state.bets[player_id] += contribution
            self.game_state.add_to_pot(contribution)
            self.game_state.current_bet = max(
                self.game_state.current_bet, self.game_state.bets[player_id]
            )
            self.game_state.last_raiser = player_id
            self.game_state.players_to_act = set(self.game_state.players_in_hand) - {
                player_id
            }
            self.game_state.record_action(action)
        else:
            raise ValueError("Unknown action.")

        if self.game_state.street == "showdown":
            return

        if not self.game_state.players_to_act:
            self.advance_street()
            return

        self.next_player()

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
            self.game_state.reset_betting_round()
            first_to_act = self._first_to_act_postflop()
            if first_to_act is None:
                self.game_state.current_player = None
            else:
                self.current_player_index = first_to_act
                self.game_state.current_player = self.players[self.current_player_index]

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
        self.showdown_hand_rank = winning_rank
        print(f"Winner: {winner} with {winning_rank}")
        self.end_hand(winner)

    def _post_blinds(self) -> None:
        if self.game_state is None:
            raise RuntimeError("Hand has not been started.")

        player_count = len(self.players)
        if player_count < 2:
            raise ValueError("Need at least two players to post blinds.")

        if player_count == 2:
            sb_index = self.dealer_index
            bb_index = (self.dealer_index + 1) % player_count
        else:
            sb_index = (self.dealer_index + 1) % player_count
            bb_index = (sb_index + 1) % player_count

        self.game_state.sb_index = sb_index
        self.game_state.bb_index = bb_index

        sb_player = self.players[sb_index]
        bb_player = self.players[bb_index]

        sb_posted = min(self.game_state.stacks[sb_player], self.small_blind)
        bb_posted = min(self.game_state.stacks[bb_player], self.big_blind)

        self.game_state.stacks[sb_player] -= sb_posted
        self.game_state.stacks[bb_player] -= bb_posted

        self.game_state.bets = {player: 0 for player in self.players}
        self.game_state.bets[sb_player] = sb_posted
        self.game_state.bets[bb_player] = bb_posted
        self.game_state.add_to_pot(sb_posted + bb_posted)
        self.game_state.current_bet = bb_posted

        first_to_act_index = self._next_active_index(bb_index)
        if first_to_act_index is None:
            self.game_state.current_player = None
        else:
            self.current_player_index = first_to_act_index
            self.game_state.current_player = self.players[self.current_player_index]

        self.game_state.players_to_act = set(self.game_state.players_in_hand) - {
            bb_player
        }

    def _first_to_act_postflop(self) -> Optional[int]:
        if self.game_state is None:
            return None

        player_count = len(self.players)
        if player_count == 2:
            return (self.dealer_index + 1) % player_count
        return self._next_active_index(self.dealer_index)

    def _next_active_index(self, start_index: int) -> Optional[int]:
        if self.game_state is None:
            return None

        player_count = len(self.players)
        if not self.game_state.players_in_hand:
            return None

        index = start_index
        for _ in range(player_count):
            index = (index + 1) % player_count
            candidate = self.players[index]
            if candidate in self.game_state.players_in_hand:
                return index
        return None

    def _award_pot(self, winner: str, hand_rank: str) -> None:
        if self.game_state is None:
            return
        self.game_state.stacks[winner] += self.game_state.pot
        self.game_state.pot = 0
        self.showdown_winner = winner
        self.showdown_hand_rank = hand_rank

    def end_hand(self, winner_id: str) -> List[str]:
        if self.game_state is None:
            return []

        if self.game_state.pot > 0:
            hand_rank = self.showdown_hand_rank or "Uncontested"
            self._award_pot(winner_id, hand_rank)

        self.game_state.last_winner = winner_id
        self.game_state.pot = 0
        self.game_state.board = []
        self.game_state.hands = {}
        self.game_state.bets = {}
        self.game_state.players_to_act = set()
        self.game_state.players_acted = set()
        self.game_state.players_in_hand = set(self.players)
        self.game_state.current_player = None
        self.game_state.current_bet = 0
        self.game_state.last_raiser = None
        self.game_state.street = "showdown"
        self.game_state.hand_number += 1

        if self.players:
            self.dealer_index = (self.dealer_index + 1) % len(self.players)

        eliminated = [
            player for player, stack in self.game_state.stacks.items() if stack == 0
        ]
        if eliminated:
            self.players = [player for player in self.players if player not in eliminated]
            for player in eliminated:
                self.game_state.stacks.pop(player, None)
            self.game_state.players = self.players
            self.game_state.players_in_hand = set(self.players)
            if self.players and self.dealer_index >= len(self.players):
                self.dealer_index = 0

        return self.players
