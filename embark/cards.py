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
    ORANGE = auto()

    def can_play(self, is_my_turn):
        if is_my_turn:
            return self in [CardColor.BLUE, CardColor.GREEN, CardColor.PURPLE]
        return self in [CardColor.BLUE, CardColor.RED]


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

    def __init__(self, color, symbol, owner, game, activation, cost, reward):
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
        """Adjust player's balances according to the rules of this card."""
        if self.color in [CardColor.BLUE, CardColor.GREEN]:
            # Funds come from the bank.
            self.owner.balance += self.get_reward()
        else:
            # Funds come from the other player
            opponent = self.get_opponent()
            available_reward = min(opponent.balance, self.get_reward())
            self.owner.balance += available_reward
            opponent.balance -= available_reward

    def get_reward(self):
        if (any(card.gives_cafe_bonus() for card in self.owner.hand) and
            self.symbol in [CardSymbol.COFFEE, CardSymbol.BREAD]):
            return self.reward + 1
        return self.reward

    def is_landmark(self):
        return False

    def enables_double_roll(self):
        return False

    def gives_extra_turn_on_doubles(self):
        return False

    def gives_cafe_bonus(self):
        return False

    def get_opponent(self):
        if self.game.active_player == self.owner:
            return self.game.inactive_player
        return self.game.active_player

    def switch_owner(self):
        opponent = self.get_opponent()
        self.owner.hand.remove(self)
        opponent.hand.append(self)
        self.owner = opponent

    def clone(self, purchaser):
        return Card(self.color,
                    self.symbol,
                    purchaser,
                    self.game,
                    self.activation,
                    self.cost,
                    self.reward)


class MultiplierCard(Card):

    def __init__(self, color, symbol, owner, game, activation, cost, multiply_on, multiply_by):
        super().__init__(color, symbol, owner, game, activation, cost, None)
        self.multiply_on = multiply_on
        self.multiply_by = multiply_by

    def activate(self):
        cards_of_symbol = len([card for card in self.owner.hand
                               if card.symbol is self.multiply_on])
        self.owner.balance += cards_of_symbol * self.multiply_by

    def clone(self, purchaser):
        return MultiplierCard(self.color,
                              self.symbol,
                              purchaser,
                              self.game,
                              self.activation,
                              self.cost,
                              self.multiply_on,
                              self.multiply_by)


class TraderCard(Card):

    def __init__(self, color, symbol, owner, game, activation, cost):
        super().__init__(color, symbol, owner, game, activation, cost, None)

    def activate(self):
        def find_tradables(player):
            return {card for card in player.hand if card.symbol is not self.symbol}

        my_tradables = find_tradables(self.owner)
        their_tradables = find_tradables(self.get_opponent())

        card_to_give = self.owner.choose_least_favorite_card(my_tradables)
        card_to_get = self.owner.choose_favorite_card(their_tradables)

        if card_to_give and card_to_get:
            card_to_give.switch_owner()
            card_to_get.switch_owner()

    def purchase(self, purchaser):
        return TraderCard(self.color,
                          self.symbol,
                          purchaser,
                          self.game,
                          self.activation,
                          self.cost)


class Landmark(Card):

    def __init__(self, player, game, cost):
        super().__init__(CardColor.ORANGE, CardSymbol.TOWER, player, game, [], cost, None)

    def is_landmark(self):
        return True


class TrainStation(Landmark):

    def __init__(self, player, game):
        super().__init__(player, game, 4)

    def enables_double_roll(self):
        return True


class ShoppingMall(Landmark):

    def __init__(self, player, game):
        super().__init__(player, game, 10)

    def gives_cafe_bonus(self):
        return True


class AmusementPark(Landmark):

    def __init__(self, player, game):
        super().__init__(player, game, 16)

    def gives_extra_turn_on_doubles(self):
        return True


class RadioTower(Landmark):

    def __init__(self, player, game):
        super().__init__(player, game, 22)


class WheatField(Card):

    def __init__(self, player, game):
        super().__init__(CardColor.BLUE, CardSymbol.WHEAT, player, game, [1], 1, 1)


class Ranch(Card):

    def __init__(self, player, game):
        super().__init__(CardColor.BLUE, CardSymbol.ANIMAL, player, game, [2], 1, 1)


class Bakery(Card):

    def __init__(self, player, game):
        super().__init__(CardColor.GREEN, CardSymbol.BREAD, player, game, [2, 3], 1, 1)


class Cafe(Card):

    def __init__(self, player, game):
        super().__init__(CardColor.RED, CardSymbol.COFFEE, player, game, [3], 2, 1)


class ConvenienceStore(Card):

    def __init__(self, player, game):
        super().__init__(CardColor.GREEN, CardSymbol.BREAD, player, game, [4], 2, 3)


class Forest(Card):

    def __init__(self, player, game):
        super().__init__(CardColor.BLUE, CardSymbol.GEAR, player, game, [5], 3, 1)


class TVStation(Card):

    def __init__(self, player, game):
        super().__init__(CardColor.PURPLE, CardSymbol.TOWER, player, game, [6], 7, 5)


class BusinessCenter(TraderCard):

    def __init__(self, player, game):
        super().__init__(CardColor.PURPLE, CardSymbol.TOWER, player, game, [6], 8)


class Stadium(Card):

    def __init__(self, player, game):
        super().__init__(CardColor.PURPLE, CardSymbol.TOWER, player, game, [6], 6, 2)


class CheeseFactory(MultiplierCard):

    def __init__(self, player, game):
        super().__init__(CardColor.GREEN, CardSymbol.FACTORY, player, game, [7], 5,
                         CardSymbol.ANIMAL, 3)


class FurnitureFactory(MultiplierCard):

    def __init__(self, player, game):
        super().__init__(CardColor.GREEN, CardSymbol.FACTORY, player, game, [8], 3,
                         CardSymbol.GEAR, 3)


class Mine(Card):

    def __init__(self, player, game):
        super().__init__(CardColor.BLUE, CardSymbol.GEAR, player, game, [9], 6, 5)


class FamilyRestaurant(Card):

    def __init__(self, player, game):
        super().__init__(CardColor.RED, CardSymbol.COFFEE, player, game, [9, 10], 3, 2)


class AppleOrchard(Card):

    def __init__(self, player, game):
        super().__init__(CardColor.BLUE, CardSymbol.WHEAT, player, game, [10], 3, 3)


class FruitAndVegetableMarket(MultiplierCard):

    def __init__(self, player, game):
        super().__init__(CardColor.GREEN, CardSymbol.FRUIT, player, game, [11, 12], 2,
                         CardSymbol.WHEAT, 2)
