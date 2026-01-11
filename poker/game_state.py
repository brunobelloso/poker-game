"""Game state container for the poker game."""


class GameState:
    def __init__(self) -> None:
        self.players = []
        self.pot = 0
        self.community_cards = []
