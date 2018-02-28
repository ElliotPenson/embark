"""
test_machi_koro.py

@author Elliot Penson
"""

import sys

from embark.machi_koro import Game, Player, LANDMARKS
from embark.cards import WheatField, Stadium

class TestGame():

    def test_purchase(self):
        game = Game(Player(), Player())
        initial_hand_size = len(game.active_player.hand)
        game.purchase_card(WheatField, game.active_player)
        final_hand_size = len(game.active_player.hand)
        assert final_hand_size == initial_hand_size + 1

    def test_invalid_purchase(self):
        game = Game(Player(), Player())
        initial_hand_size = len(game.active_player.hand)
        game.purchase_card(Stadium, game.active_player)
        final_hand_size = len(game.active_player.hand)
        # A stadium is too expensive for a new player.
        assert final_hand_size == initial_hand_size

    def test_landmark_purchase(self):
        game = Game(Player(), Player())
        game.active_player.balance = sys.maxsize  # Give the player enough money to buy anything.
        for landmark in LANDMARKS:
            assert landmark in game.find_available_cards(game.active_player)
            game.purchase_card(landmark, game.active_player)
            # Landmarks can only be purchased once.
            assert landmark not in game.find_available_cards(game.active_player)


class TestPlayer():

    def test_win_condition(self):
        player = Player()
        player.hand = []
        assert not player.has_won()
        player.hand = [landmark(player, None) for landmark in LANDMARKS]
        assert player.has_won()
