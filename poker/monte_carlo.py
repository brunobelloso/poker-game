"""Monte Carlo equity estimation for Texas Hold'em."""

from __future__ import annotations

import random

from poker.cards import Card, RANKS, SUITS
from poker.hand_evaluator import evaluate_hand


def estimate_equity(
    hero_cards: list[Card],
    board_cards: list[Card],
    iterations: int = 300,
) -> float:
    if iterations <= 0:
        return 0.0

    used_cards = {(card.rank, card.suit) for card in hero_cards + board_cards}
    deck = [
        Card(rank=rank, suit=suit)
        for rank in RANKS
        for suit in SUITS
        if (rank, suit) not in used_cards
    ]

    wins = 0
    ties = 0
    missing_board = max(0, 5 - len(board_cards))

    for _ in range(iterations):
        drawn = random.sample(deck, 2 + missing_board)
        opponent_cards = drawn[:2]
        board_fill = drawn[2:]
        full_board = list(board_cards) + board_fill

        hero_score = evaluate_hand(hero_cards + full_board)
        opponent_score = evaluate_hand(opponent_cards + full_board)

        if hero_score > opponent_score:
            wins += 1
        elif hero_score == opponent_score:
            ties += 1

    return (wins + 0.5 * ties) / iterations
