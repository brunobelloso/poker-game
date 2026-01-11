"""Deck implementation for the poker game."""

from typing import List

from .cards import Card


class Deck:
    def __init__(self) -> None:
        self._cards: List[Card] = []

    def shuffle(self) -> None:
        raise NotImplementedError

    def deal(self, count: int = 1) -> List[Card]:
        raise NotImplementedError
