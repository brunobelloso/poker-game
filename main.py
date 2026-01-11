"""Entry point for the poker game."""

from poker.actions import Action, ActionType
from poker.deck import Deck
from poker.game_state import GameState


def main() -> None:
    deck = Deck()
    deck.shuffle()

    players = ["Alice", "Bob"]
    stacks = {"Alice": 1000, "Bob": 1000}
    hands = {player: deck.deal(2) for player in players}

    game_state = GameState(
        players=players,
        stacks=stacks,
        pot=0,
        board=[],
        hands=hands,
        current_player="Alice",
        street="preflop",
    )
    game_state.record_action(Action(ActionType.CALL))
    print(game_state)


if __name__ == "__main__":
    main()
