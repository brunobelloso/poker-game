"""Human player implementation."""

from poker.actions import Action, ActionType
from poker.game_state import GameState
from poker.players.base_player import BasePlayer


class HumanPlayer(BasePlayer):
    def decide(self, game_state: GameState):
        while True:
            to_call = game_state.to_call(self.id)

            if to_call > 0:
                legal = {"call", "raise", "fold"}
            else:
                legal = {"check", "raise", "fold"}

            print(f"Legal actions: {', '.join(sorted(legal))}")
            choice = input("Enter action: ").strip().lower()

            if choice not in legal:
                print(f"Invalid action. Legal actions are: {', '.join(sorted(legal))}")
                continue

            if choice == "call":
                return Action(ActionType.CALL)
            if choice == "check":
                return Action(ActionType.CHECK)
            if choice == "fold":
                return Action(ActionType.FOLD)
            if choice == "raise":
                raise_to = int(input("Raise to amount: "))
                return Action(ActionType.RAISE, amount=raise_to)
