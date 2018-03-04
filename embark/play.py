"""
play.py

@author Elliot Penson
"""

from collections import Counter

from prettytable import PrettyTable
import inquirer

from embark.machi_koro import Game, Player


class Human(Player):

    def construct(self, available):
        """Display player statistics and prompt for a card."""
        self.display_hand()
        self.display_balance()
        below_balance = {card for card in available
                         if card(self, self.game).cost <= self.balance}
        return prompt(below_balance,
                      "Which card would you like to buy?",
                      lambda card: card.__name__)

    def display_hand(self):
        """Print a table of card types and the number owned by the player."""
        print("Your current hand:")
        table = PrettyTable(["Card", "Count"])
        counts = Counter(card.__class__.__name__ for card in self.hand)
        for card_name in counts:
            table.add_row([card_name, counts[card_name]])
        print(table, end="\n\n")

    def display_balance(self):
        print(f"You have {self.balance} coin{'' if self.balance == 1 else 's'}.")

    def choose_favorite_card(self, cards):
        return prompt(cards, "Which card is your favorite?", lambda card: card.__class__.__name__)

    def choose_least_favorite_card(self, cards):
        return prompt(cards,
                      "Which card is your least favorite?",
                      lambda card: card.__class__.__name__)


def human_vs_computer(organism):
    game = Game(organism, Human())
    game.simulate()
    if game.winner == organism:
        print("You lost!")
    else:
        print("You won!")


def prompt(items, message, key=None):
    """Ask the user to select an item from a list."""
    if not key:
        key = lambda x: x

    key_to_item = {key(item): item for item in items}
    questions = [
        inquirer.List("choice",
                      message=message,
                      choices=list(key_to_item.keys()) + [None])
    ]
    choice = inquirer.prompt(questions)["choice"]
    if choice:
        return key_to_item[choice]
