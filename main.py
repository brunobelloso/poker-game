"""Entry point for the poker game."""

from poker.actions import Action, ActionType
from poker.engine import PokerEngine


def main() -> None:
    engine = PokerEngine(players=["P1", "P2"], starting_stack=1000)
    engine.start_hand()

    while engine.game_state and engine.game_state.street != "showdown":
        current_player = engine.game_state.current_player
        engine.apply_action(current_player, Action(ActionType.CHECK))
        print(engine.game_state)


if __name__ == "__main__":
    main()
