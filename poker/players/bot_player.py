"""Bot player implementation."""

from poker.actions import Action, ActionType
from poker.cards import Card, RANKS, SUITS
from poker.game_state import GameState
from poker.hand_evaluator import HIGH_CARD, ONE_PAIR, TWO_PAIR, evaluate_hand
from poker.players.base_player import BasePlayer


class BotPlayer(BasePlayer):
    def decide(self, game_state: GameState):
        legal_actions = self._get_legal_actions()
        legal_types = {action.type for action in legal_actions}

        hole_cards = game_state.hands.get(self.id, [])
        if len(hole_cards) < 2:
            return self._pick_action(legal_types, ActionType.CHECK)

        if game_state.street == "preflop":
            return self._decide_preflop(hole_cards, legal_types)

        combined = hole_cards + game_state.board
        filled = self._complete_to_seven_cards(combined)
        hand_rank = evaluate_hand(filled)[0]
        call_amount = 10
        if hand_rank >= TWO_PAIR:
            return self._pick_action(legal_types, ActionType.RAISE, amount=10)
        if hand_rank == ONE_PAIR:
            return self._pick_action(
                legal_types, ActionType.CHECK, fallback=ActionType.CALL
            )
        if hand_rank == HIGH_CARD:
            has_draw = self.detect_flush_draw(combined) or self.detect_straight_draw(
                combined
            )
            if has_draw:
                pot_odds = self.calculate_pot_odds(game_state, call_amount)
                if pot_odds <= 0.35:
                    return self._pick_action(
                        legal_types, ActionType.CALL, fallback=ActionType.CHECK
                    )
            return self._pick_action(legal_types, ActionType.FOLD)

        return self._pick_action(legal_types, ActionType.CHECK)

    def _get_legal_actions(self):
        if self.engine and hasattr(self.engine, "get_legal_actions"):
            return self.engine.get_legal_actions(self.id)
        return [Action(action_type) for action_type in ActionType]

    def calculate_pot_odds(self, game_state: GameState, call_amount: int) -> float:
        return call_amount / (game_state.pot + call_amount)

    def detect_flush_draw(self, cards: list[Card]) -> bool:
        suit_counts = {suit: 0 for suit in SUITS}
        for card in cards:
            suit_counts[card.suit] += 1
        return any(count == 4 for count in suit_counts.values())

    def detect_straight_draw(self, cards: list[Card]) -> bool:
        rank_values = {rank: index + 2 for index, rank in enumerate(RANKS)}
        values = {rank_values[card.rank] for card in cards}
        if "A" in {card.rank for card in cards}:
            values.add(1)
        for value in values:
            if all((value + offset) in values for offset in range(4)):
                return True
        return False

    def _decide_preflop(self, hole_cards, legal_types):
        ranks = [card.rank for card in hole_cards]
        rank_set = frozenset(ranks)

        strong_pairs = {"A", "K", "Q", "J"}
        medium_pairs = {"10", "9", "8"}
        strong_offsuit = {frozenset({"A", "K"})}
        medium_offsuit = {
            frozenset({"A", "Q"}),
            frozenset({"A", "J"}),
            frozenset({"K", "Q"}),
        }

        if len(rank_set) == 1:
            pair_rank = ranks[0]
            if pair_rank in strong_pairs:
                return self._pick_action(legal_types, ActionType.RAISE, amount=10)
            if pair_rank in medium_pairs:
                return self._pick_action(
                    legal_types, ActionType.CHECK, fallback=ActionType.CALL
                )
            return self._pick_action(legal_types, ActionType.FOLD)

        if rank_set in strong_offsuit:
            return self._pick_action(legal_types, ActionType.RAISE, amount=10)
        if rank_set in medium_offsuit:
            return self._pick_action(legal_types, ActionType.CHECK, fallback=ActionType.CALL)

        return self._pick_action(legal_types, ActionType.FOLD)

    def _complete_to_seven_cards(self, cards):
        if len(cards) >= 7:
            return cards[:7]

        existing = {(card.rank, card.suit) for card in cards}
        existing_ranks = {card.rank for card in cards}
        filled = list(cards)

        for rank in RANKS:
            if rank in existing_ranks:
                continue
            for suit in SUITS:
                candidate = (rank, suit)
                if candidate in existing:
                    continue
                filled.append(Card(rank=rank, suit=suit))
                existing.add(candidate)
                if len(filled) == 7:
                    return filled

        return filled

    def _pick_action(self, legal_types, primary, amount=None, fallback=None):
        if primary in legal_types:
            return Action(primary, amount if primary == ActionType.RAISE else None)
        if fallback and fallback in legal_types:
            return Action(fallback)
        if ActionType.CHECK in legal_types:
            return Action(ActionType.CHECK)
        if ActionType.CALL in legal_types:
            return Action(ActionType.CALL)
        return Action(ActionType.FOLD)
