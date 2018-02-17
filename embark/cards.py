"""
cards.py

@author Elliot Penson
"""

from enum import Enum, auto


class CardColor(Enum):
    BLUE = auto()
    GREEN = auto()
    RED = auto()
    PURPLE = auto()

    def can_play(self, is_my_turn):
        if is_my_turn:
            return self in [CardColor.BLUE, CardColor.RED]
        return self in [CardColor.GREEN, CardColor.PURPLE]


class CardType(Enum):
    FIELD = auto()
    RANCH = auto()
    BAKER = auto()
    CAFE = auto()
    CONVENIENCE_STORE = auto()
    FOREST = auto()
    TV_STATION = auto()
    BUSINESS_CENTER = auto()
    STADIUM = auto()
    CHEESE_FACTORY = auto()
    FURNITURE_FACTORY = auto()
    MINE = auto()
    FAMILY_RESTAURANT = auto()
    APPLE_ORCHARD = auto()
    FRUIT_VEG_MARKET = auto()


class CardSymbol(Enum):
    WHEAT = auto()
    ANIMAL = auto()
    BREAD = auto()
    COFFEE = auto()
    GEAR = auto()
    TOWER = auto()
    FACTORY = auto()
    FRUIT = auto()


class Card:

    def __init__(self, card_type, color, symbol, owner, game, activation, cost, reward):
        self.card_type = card_type
        self.color = color
        self.symbol = symbol
        self.owner = owner
        self.game = game
        self.activation = activation
        self.cost = cost
        self.reward = reward

    def notify(self, roll):
        """React to a roll."""
        if not self.owner:
            raise RuntimeError("This card has not been purchased!")

        is_owners_turn = self.game.active_player == self.owner
        if roll in self.activation and self.color.can_play(is_owners_turn):
            self.activate()

    def activate(self):
        """Adjust player's balances according to the roles of this card."""
        if self.color in [CardColor.BLUE, CardColor.GREEN]:
            # Funds come from the bank.
            self.owner.balance += self.reward
        else:
            # Funds come from the other player
            opponent = self.get_opponent()
            available_reward = min(opponent.balance, self.reward)
            self.owner.balance += available_reward
            opponent.balance -= available_reward

    def get_opponent(self):
        if self.game.active_player == self.owner:
            return self.game.inactive_player
        return self.game.active_player
