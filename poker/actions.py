"""Action definitions for the poker game."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ActionType(Enum):
    FOLD = "fold"
    CHECK = "check"
    CALL = "call"
    RAISE = "raise"


@dataclass(frozen=True)
class Action:
    type: ActionType
    amount: Optional[int] = None

    def __repr__(self) -> str:
        if self.amount is None:
            return self.type.name
        return f"{self.type.name}({self.amount})"
