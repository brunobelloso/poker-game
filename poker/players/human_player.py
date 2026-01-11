"""Human player implementation."""

from poker.actions import Action, ActionType
from poker.game_state import GameState
from poker.players.base_player import BasePlayer


class HumanPlayer(BasePlayer):
    def decide(self, game_state: GameState):
        print(game_state)
        if self.engine and hasattr(self.engine, "get_legal_actions"):
            legal_actions = self.engine.get_legal_actions(self.id)
        else:
            legal_actions = list(ActionType)
        to_call = game_state.to_call(self.id)
        print(
            f"Current bet: {game_state.current_bet} | To call: {to_call} | "
            f"Legal actions: {legal_actions}"
        )
        choice = input("Enter action (check, call, raise, fold): ").strip().lower()
        if choice == "raise":
            amount = int(input("Raise to amount: ").strip())
            return Action(ActionType.RAISE, amount)
        return Action(ActionType(choice))
