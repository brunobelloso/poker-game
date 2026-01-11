"""Action definitions for the poker game."""

from enum import Enum


class Action(Enum):
    FOLD = "fold"
    CALL = "call"
    RAISE = "raise"
    CHECK = "check"
