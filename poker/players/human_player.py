"""Human player implementation."""

from poker.actions import Action, ActionType
from poker.game_state import GameState
from poker.players.base_player import BasePlayer


class HumanPlayer(BasePlayer):
    def decide(self, game_state: GameState):
        print(game_state)
        to_call = game_state.to_call(self.id)
        if self.engine and hasattr(self.engine, "get_legal_actions"):
            legal_actions = set(self.engine.get_legal_actions(self.id))
        else:
            if to_call == 0:
                legal_actions = {ActionType.CHECK, ActionType.RAISE, ActionType.FOLD}
            else:
                legal_actions = {ActionType.CALL, ActionType.RAISE, ActionType.FOLD}
        print(
            f"Current bet: {game_state.current_bet} | To call: {to_call} | "
            f"Legal actions: {legal_actions}"
        )
        action_map = {
            "check": ActionType.CHECK,
            "call": ActionType.CALL,
            "raise": ActionType.RAISE,
            "fold": ActionType.FOLD,
        }
        legal_action_names = ", ".join(action.name for action in legal_actions)
        while True:
            choice = input("Enter action (check, call, raise, fold): ").strip().lower()
            action_type = action_map.get(choice)
            if action_type is None:
                print(f"Invalid action. Legal actions are: {legal_action_names}.")
                continue
            if action_type == ActionType.CALL and to_call == 0:
                print(f"Invalid action. Legal actions are: {legal_action_names}.")
                continue
            if action_type == ActionType.CHECK and to_call > 0:
                print(f"Invalid action. Legal actions are: {legal_action_names}.")
                continue
            if action_type not in legal_actions:
                print(f"Invalid action. Legal actions are: {legal_action_names}.")
                continue
            if action_type == ActionType.RAISE:
                while True:
                    amount_input = input("Raise to amount: ").strip()
                    try:
                        amount = int(amount_input)
                    except ValueError:
                        print("Invalid raise amount. Enter a whole number.")
                        continue
                    return Action(ActionType.RAISE, amount)
            return Action(action_type)
