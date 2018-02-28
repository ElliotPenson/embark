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
