"""Entry point for the poker game."""

from poker.engine import PokerEngine
from poker.players.bot_player import BotPlayer
from poker.players.human_player import HumanPlayer


def main() -> None:
    player_one = HumanPlayer("P1")
    player_two = BotPlayer("P2")
    player_three = BotPlayer("P3")
    player_four = BotPlayer("P4")
    players = [player_one, player_two, player_three, player_four]
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

    if engine.game_state and engine.game_state.street == "showdown":
        board = " ".join(str(card) for card in engine.game_state.board)
        print(f"Final board: {board}")
        for player in players:
            hand = " ".join(str(card) for card in engine.game_state.hands[player.id])
            print(f"{player.id} hand: {hand}")
        if engine.showdown_winner and engine.showdown_hand_rank:
            print(
                f"Winner: {engine.showdown_winner} ({engine.showdown_hand_rank})"
            )


if __name__ == "__main__":
    main()
