"""Entry point for the poker game."""
from poker.engine import PokerEngine
from poker.players.bot_player import BotPlayer
from poker.players.human_player import HumanPlayer


def main() -> None:
    player_one = HumanPlayer("P1")
    player_two = BotPlayer("P2", style="tight")
    player_three = BotPlayer("P3", style="loose")
    player_four = BotPlayer("P4", style="aggro")
    players = [player_one, player_two, player_three, player_four]
    engine = PokerEngine(players=[player.id for player in players], starting_stack=1000)
    for player in players:
        player.engine = engine
    player_by_id = {player.id: player for player in players}

    while True:
        engine.start_hand()
        if engine.game_state is None:
            print("Unable to start a new hand.")
            return
        print(f"=== HAND {engine.game_state.hand_number + 1} ===")

        while engine.game_state and engine.game_state.street != "showdown":
            current_player_id = engine.game_state.current_player
            if current_player_id is None:
                break
            current_player = player_by_id[current_player_id]
            action = current_player.decide(engine.game_state)
            engine.apply_action(current_player.id, action)
            print(engine.game_state)

        if engine.game_state is None:
            return

        if engine.game_state.last_winner:
            print(f"Hand winner: {engine.game_state.last_winner}")

        if engine.game_state.side_pots:
            print("Side pots:")
            for idx, pot in enumerate(engine.game_state.side_pots, start=1):
                eligible = ", ".join(sorted(pot["eligible"]))
                print(f"  Pot {idx}: {pot['amount']} | Eligible: {eligible}")

        if engine.game_state.total_contrib:
            print("Total contributions:")
            for player_id, amount in engine.game_state.total_contrib.items():
                print(f"{player_id}: {amount}")

        print("Updated stacks:")
        for player_id, stack in engine.game_state.stacks.items():
            print(f"{player_id}: {stack}")

        human_stack = engine.game_state.stacks.get(player_one.id, 0)
        if human_stack == 0:
            print("You are busted.")
            return

        if len(engine.players) == 1:
            print(f"{engine.players[0]} wins the table.")
            return

        play_next = input("Play next hand? (y/n): ").strip().lower()
        if play_next != "y":
            print("Exiting game.")
            return


if __name__ == "__main__":
    main()
