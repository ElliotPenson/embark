"""
test_cards.py

@author Elliot Penson
"""

from embark.cards import (Card, TrainStation, ShoppingMall, AmusementPark, RadioTower, WheatField,
                          Ranch, Bakery, Cafe, ConvenienceStore, Forest, TVStation, BusinessCenter,
                          Stadium, CheeseFactory, FurnitureFactory, Mine, FamilyRestaurant,
                          AppleOrchard, FruitAndVegetableMarket, CardColor, CardSymbol)
from embark.machi_koro import Game, Player


def test_is_landmark():
    landmarks = [TrainStation, ShoppingMall, AmusementPark, RadioTower]
    establishments = [WheatField, Ranch, Bakery, Cafe, ConvenienceStore, Forest, TVStation,
                      BusinessCenter, Stadium, CheeseFactory, FurnitureFactory, Mine,
                      FamilyRestaurant, AppleOrchard, FruitAndVegetableMarket]
    for landmark in landmarks:
        assert landmark(None, None).is_landmark()
    for establishment in establishments:
        assert not establishment(None, None).is_landmark()


def test_enables_double_roll():
    assert TrainStation(None, None).enables_double_roll()
    single_roll_cards = [ShoppingMall, AmusementPark, RadioTower, WheatField, Ranch, Bakery, Cafe,
                         ConvenienceStore, Forest, TVStation, BusinessCenter, Stadium,
                         CheeseFactory, FurnitureFactory, Mine, FamilyRestaurant, AppleOrchard,
                         FruitAndVegetableMarket]
    for card in single_roll_cards:
        assert not card(None, None).enables_double_roll()


def test_notify():
    game = Game(Player(), Player())
    card = WheatField(game.active_player, game)
    initial_balance = game.active_player.balance
    card.notify(card.activation[0])
    final_balance = game.active_player.balance
    assert final_balance > initial_balance


class MockPlayer(Player):

    def choose_favorite_card(self, cards):
        return next(card for card in cards if card.__class__ is WheatField)

    def choose_least_favorite_card(self, cards):
        return next(card for card in cards if card.__class__ is Bakery)


def test_trading():
    game = Game(MockPlayer(), MockPlayer())
    card = BusinessCenter(game.active_player, game)
    card.notify(card.activation[0])
    assert all(card.__class__ is WheatField for card in game.active_player.hand)
    assert all(card.__class__ is Bakery for card in game.inactive_player.hand)
