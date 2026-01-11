"""Human player implementation."""

from poker.actions import Action, ActionType
from poker.game_state import GameState
from poker.players.base_player import BasePlayer


class HumanPlayer(BasePlayer):
    def decide(self, game_state: GameState):
        print(game_state)
        to_call = game_state.to_call(self.id)
        if to_call > 0:
            legal_actions = {"call", "raise", "fold"}
        else:
            legal_actions = {"check", "raise", "fold"}
        print(
            f"Current bet: {game_state.current_bet} | To call: {to_call} | "
            f"Legal actions: {legal_actions}"
        )
        legal_action_names = ", ".join(sorted(legal_actions))
        while True:
            choice = input("Enter action (check, call, raise, fold): ").strip().lower()
            if choice not in legal_actions:
                print(f"Invalid action. Legal actions are: {legal_action_names}.")
                continue
            if choice == "raise":
                while True:
                    amount_input = input("Raise to amount: ").strip()
                    try:
                        amount = int(amount_input)
                    except ValueError:
                        print("Invalid raise amount. Enter a whole number.")
                        continue
                    return Action(ActionType.RAISE, amount)
            if choice == "call":
                return Action(ActionType.CALL)
            if choice == "check":
                return Action(ActionType.CHECK)
            return Action(ActionType.FOLD)
