"""
machi_koro.py

@author Elliot Penson
"""

import random

from embark import cards


def make_random_genes():
    genes = {
        cards.TrainStation: random.random(),
        cards.ShoppingMall: random.random(),
        cards.AmusementPark: random.random(),
        cards.RadioTower: random.random(),
        cards.WheatField: random.random(),
        cards.Ranch: random.random(),
        cards.Bakery: random.random(),
        cards.Cafe: random.random(),
        cards.ConvenienceStore: random.random(),
        cards.Forest: random.random(),
        cards.TVStation: random.random(),
        cards.BusinessCenter: random.random(),
        cards.Stadium: random.random(),
        cards.CheeseFactory: random.random(),
        cards.FurnitureFactory: random.random(),
        cards.Mine: random.random(),
        cards.FamilyRestaurant: random.random(),
        cards.AppleOrchard: random.random(),
        cards.FruitAndVegetableMarket: random.random()
    }
    return normalize(genes)


def select_card(genes):
    """Choose a card by referencing a strategy. The genes parameter is a dictionary from
    card class -> probability of selection.
    """
    if sum(genes.values()) == 0:
        return random.choice(genes)  # Choose an arbitrary card.

    genes = normalize(genes)
    running_total = 0
    sample = random.random()
    for card in genes:
        running_total += genes[card]
        if running_total >= sample:
            return card


def normalize(genes):
    """Make all probabilities sum to one."""
    total = sum(genes.values())
    return {card: probability / total for card, probability in genes.items()}
