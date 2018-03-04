"""
machi_koro.py

@author Elliot Penson
"""

from collections import Counter
from random import randint

from embark import cards

ALL_CARDS = [cards.TrainStation, cards.ShoppingMall, cards.AmusementPark, cards.RadioTower,
             cards.WheatField, cards.Ranch, cards.Bakery, cards.Cafe, cards.ConvenienceStore,
             cards.Forest, cards.TVStation, cards.BusinessCenter, cards.Stadium,
             cards.CheeseFactory, cards.FurnitureFactory, cards.Mine, cards.FamilyRestaurant,
             cards.AppleOrchard, cards.FruitAndVegetableMarket]
STARTING_ESTABLISHMENTS = {
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
        self.establishments = Counter(STARTING_ESTABLISHMENTS)
        self.landmarks = {player1: set(LANDMARKS), player2: set(LANDMARKS)}

    def find_available_cards(self, player):
        return set(self.establishments.elements()) | self.landmarks[player]

    def purchase_card(self, card_class, player):
        """A factory method that creates cards and lowers the inventory count."""
        if card_class not in self.find_available_cards(player):
            raise RuntimeError("Tried to buy a card that isn't available!")

        instance = card_class(player, self)
        if player.has_funds_for(instance):
            if instance.is_landmark():
                self.landmarks[player].remove(card_class)
            else:
                self.establishments[card_class] -= 1
            player.receive_card(instance)

    def switch_player(self):
        self.active_player, self.inactive_player = self.inactive_player, self.active_player

    def simulate_round(self):
        """Perform roll, earn, and construct stages of a round."""
        roll_number, was_double = self.active_player.roll()

        self.active_player.earn(roll_number)
        self.inactive_player.earn(roll_number)

        available_cards = self.find_available_cards(self.active_player)
        card_class = self.active_player.construct(available_cards)
        if card_class:
            self.purchase_card(card_class, self.active_player)

        if self.active_player.has_won():
            self.winner = self.active_player

        if not (was_double and any(card.gives_extra_turn_on_doubles()
                                   for card in self.active_player.hand)):
            self.switch_player()

    def simulate(self):
        while not self.winner:
            self.simulate_round()


class Player:

    def __init__(self):
        self.wins = 0

    def join_game(self, game):
        self.game = game
        self.hand = [cards.WheatField(self, game), cards.Bakery(self, game)]
        self.balance = STARTING_BALANCE

    def has_won(self):
        return len([card for card in self.hand if card.is_landmark()]) == len(LANDMARKS)

    def has_card(self, card_class):
        return any(card.__class__ == card_class for card in self.hand)

    def has_funds_for(self, card):
        return card.cost <= self.balance

    def receive_card(self, card):
        self.hand.append(card)
        self.balance -= card.cost

    def roll(self):
        """Throw the dice. Return a (number, was_double) tuple."""
        first_roll = roll()
        if any(card.enables_double_roll() for card in self.hand):
            second_roll = roll()
            return first_roll + second_roll, first_roll == second_roll
        return first_roll, False

    def earn(self, roll_number):
        """Tell all card observers about a roll and earn money accordingly."""
        for card in self.hand:
            card.notify(roll_number)

    def choose_favorite_card(self, cards):
        raise NotImplementedError()

    def choose_least_favorite_card(self, cards):
        raise NotImplementedError()

    def construct(self, available):
        """Abstract method. Return a card class from the given list."""
        raise NotImplementedError()


def roll(number_of_die_faces=6):
    return randint(1, number_of_die_faces)
