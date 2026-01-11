"""Texas Hold'em hand evaluator."""

from __future__ import annotations

from collections import Counter
from itertools import combinations
from typing import Iterable, List, Tuple

from .cards import Card, RANKS

HIGH_CARD = 1
ONE_PAIR = 2
TWO_PAIR = 3
THREE_OF_A_KIND = 4
STRAIGHT = 5
FLUSH = 6
FULL_HOUSE = 7
FOUR_OF_A_KIND = 8
STRAIGHT_FLUSH = 9

HAND_RANK_NAMES = {
    HIGH_CARD: "High Card",
    ONE_PAIR: "One Pair",
    TWO_PAIR: "Two Pair",
    THREE_OF_A_KIND: "Three of a Kind",
    STRAIGHT: "Straight",
    FLUSH: "Flush",
    FULL_HOUSE: "Full House",
    FOUR_OF_A_KIND: "Four of a Kind",
    STRAIGHT_FLUSH: "Straight Flush",
}

RANK_VALUES = {rank: index for index, rank in enumerate(RANKS, start=2)}


def evaluate_hand(cards: List[Card]) -> Tuple[int, ...]:
    if len(cards) != 7:
        raise ValueError("evaluate_hand expects exactly 7 cards")

    best: Tuple[int, ...] = ()
    for combo in combinations(cards, 5):
        score = _evaluate_five(combo)
        if not best or score > best:
            best = score
    return best


def _evaluate_five(cards: Iterable[Card]) -> Tuple[int, ...]:
    ranks = sorted((RANK_VALUES[card.rank] for card in cards), reverse=True)
    suits = {card.suit for card in cards}
    counts = Counter(ranks)

    is_flush = len(suits) == 1
    is_straight, straight_high = _is_straight(ranks)

    if is_flush and is_straight:
        return (STRAIGHT_FLUSH, straight_high)

    if 4 in counts.values():
        four_rank = max(rank for rank, count in counts.items() if count == 4)
        kicker = max(rank for rank, count in counts.items() if count == 1)
        return (FOUR_OF_A_KIND, four_rank, kicker)

    if sorted(counts.values()) == [2, 3]:
        three_rank = max(rank for rank, count in counts.items() if count == 3)
        pair_rank = max(rank for rank, count in counts.items() if count == 2)
        return (FULL_HOUSE, three_rank, pair_rank)

    if is_flush:
        return (FLUSH, *sorted(ranks, reverse=True))

    if is_straight:
        return (STRAIGHT, straight_high)

    if 3 in counts.values():
        three_rank = max(rank for rank, count in counts.items() if count == 3)
        kickers = sorted(
            (rank for rank, count in counts.items() if count == 1), reverse=True
        )
        return (THREE_OF_A_KIND, three_rank, *kickers)

    if list(counts.values()).count(2) == 2:
        pair_ranks = sorted(
            (rank for rank, count in counts.items() if count == 2), reverse=True
        )
        kicker = max(rank for rank, count in counts.items() if count == 1)
        return (TWO_PAIR, *pair_ranks, kicker)

    if 2 in counts.values():
        pair_rank = max(rank for rank, count in counts.items() if count == 2)
        kickers = sorted(
            (rank for rank, count in counts.items() if count == 1), reverse=True
        )
        return (ONE_PAIR, pair_rank, *kickers)

    return (HIGH_CARD, *sorted(ranks, reverse=True))


def _is_straight(ranks: List[int]) -> Tuple[bool, int]:
    unique = sorted(set(ranks), reverse=True)
    if len(unique) != 5:
        return False, 0

    if unique == [14, 5, 4, 3, 2]:
        return True, 5

    if unique[0] - unique[-1] == 4:
        return True, unique[0]

    return False, 0
