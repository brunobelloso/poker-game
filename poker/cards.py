"""Card definitions for the poker game."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Card:
    rank: str
    suit: str
