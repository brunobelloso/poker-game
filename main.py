"""Entry point for the poker game."""

from poker.deck import Deck


def main() -> None:
    deck = Deck()
    deck.shuffle()
    dealt = deck.deal(2)
    print(f"Dealt cards: {dealt}")


if __name__ == "__main__":
    main()
