"""Entry point for the poker game."""

from poker.engine import PokerEngine
from poker.players.bot_player import BotPlayer
from poker.players.human_player import HumanPlayer


def main() -> None:
    player_one = HumanPlayer("P1")
    player_two = BotPlayer("P2")
    players = [player_one, player_two]
    engine = PokerEngine(players=[player.id for player in players], starting_stack=1000)
    for player in players:
        player.engine = engine
    engine.start_hand()

    while engine.game_state and engine.game_state.street != "showdown":
        current_player_id = engine.game_state.current_player
        current_player = next(
            player for player in players if player.id == current_player_id
        )
        action = current_player.decide(engine.game_state)
        engine.apply_action(current_player_id, action)
        print(engine.game_state)


if __name__ == "__main__":
    main()
