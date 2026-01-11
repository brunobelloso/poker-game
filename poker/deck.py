"""Deck implementation for the poker game."""

import random
from typing import List, Union

from .cards import RANKS, SUITS, Card


class Deck:
    def __init__(self) -> None:
        self._cards: List[Card] = [
            Card(rank=rank, suit=suit) for suit in SUITS for rank in RANKS
        ]

    def shuffle(self) -> None:
        random.shuffle(self._cards)

    def deal(self, count: int = 1) -> Union[Card, List[Card]]:
        if not self._cards:
            raise ValueError("Cannot deal from an empty deck.")
        if count < 1:
            raise ValueError("Deal count must be at least 1.")
        if count > len(self._cards):
            raise ValueError("Not enough cards left in the deck.")

        if count == 1:
            return self._cards.pop()

        dealt_cards = self._cards[-count:]
        del self._cards[-count:]
        return dealt_cards
