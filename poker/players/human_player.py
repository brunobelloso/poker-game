"""Human player implementation."""

from poker.actions import Action, ActionType
from poker.game_state import GameState
from poker.players.base_player import BasePlayer


class HumanPlayer(BasePlayer):
    def decide(self, game_state: GameState):
        print(game_state)
        legal_actions = None
        if self.engine and hasattr(self.engine, "get_legal_actions"):
            legal_actions = self.engine.get_legal_actions(self.id)
        else:
            legal_actions = [Action(action_type) for action_type in ActionType]
        print(f"Legal actions: {legal_actions}")
        choice = input("Enter action (check, call, raise, fold): ").strip().lower()
        if choice == "raise":
            amount = int(input("Raise amount: ").strip())
            return Action(ActionType.RAISE, amount)
        return Action(ActionType(choice))
