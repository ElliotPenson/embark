"""
machi_koro.py

@author Elliot Penson
"""

from collections import Counter
from random import randint

from embark import cards
from embark.evolution import select_card

STARTING_INVENTORY = {
    cards.TrainStation: 2,
    cards.ShoppingMall: 2,
    cards.AmusementPark: 2,
    cards.RadioTower: 2,
    cards.WheatField: 6,
    cards.Ranch: 6,
    cards.Bakery: 6,
    cards.Cafe: 6,
    cards.ConvenienceStore: 6,
    cards.Forest: 6,
    cards.TVStation: 4,
    cards.BusinessCenter: 4,
    cards.Stadium: 4,
    cards.CheeseFactory: 6,
    cards.FurnitureFactory: 6,
    cards.Mine: 6,
    cards.FamilyRestaurant: 6,
    cards.AppleOrchard: 6,
    cards.FruitAndVegetableMarket: 6
}
STARTING_BALANCE = 3
LANDMARKS = [cards.TrainStation, cards.ShoppingMall, cards.AmusementPark, cards.RadioTower]


class Game:

    def __init__(self, player1, player2):
        player1.join_game(self)
        player2.join_game(self)
        self.active_player = player1
        self.inactive_player = player2
        self.winner = None
        self.cards = Counter(STARTING_INVENTORY)

    def find_available_cards(self):
        return set(self.cards.elements())

    def purchase_card(self, card, player):
        """A factory method that creates cards and lowers the inventory count."""
        if card not in self.find_available_cards():
            raise RuntimeError("Tried to buy a card that isn't available!")

        instance = card(player, self)
        if player.can_buy(instance):
            self.cards[card] -= 1
            return instance

    def switch_player(self):
        self.active_player, self.inactive_player = self.active_player, self.inactive_player

    def simulate_round(self):
        """Perform roll, earn, and construct stages of a round."""
        self.switch_player()
        roll_number = self.active_player.roll()

        self.active_player.earn(roll_number)
        self.inactive_player.earn(roll_number)

        available_cards = self.find_available_cards()
        self.active_player.construct(available_cards)

        if self.active_player.has_won():
            self.winner = self.active_player

    def simulate(self):
        while not self.winner:
            self.simulate_round()


class Player:

    def __init__(self, genes):
        """Create an AI that plays Machi Koro by referencing a gene dictionary (card ->
        probability of purchase).
        """
        self.genes = genes

    def join_game(self, game):
        self.game = game
        self.hand = [cards.WheatField(self, game), cards.Bakery(self, game)]
        self.balance = STARTING_BALANCE

    def has_won(self):
        return len([card.is_winning() for card in self.hand]) == len(LANDMARKS)

    def can_buy(self, card):
        return card.cost <= self.balance

    def roll(self):
        number = roll()
        if any(card.enables_double_roll() for card in self.hand):
            number += roll()
        return number

    def earn(self, roll_number):
        """Tell all card observers about a roll and earn money accordingly."""
        for card in self.hand:
            card.notify(roll_number)

    def construct(self, available):
        """Sample from this player's genes to select and purchase a card."""
        relevant_genes = {card: probability for card, probability in self.genes.items()
                          if card in available}
        card = select_card(relevant_genes)
        instance = self.game.purchase_card(card, self)
        if instance:
            self.hand.append(instance)
            self.balance -= instance.cost


def roll(number_of_die_faces=6):
    return randint(1, number_of_die_faces)
