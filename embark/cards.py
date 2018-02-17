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
