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
        card_name_to_class = {card.__name__: card for card in available
                              if card(self, self.game).cost <= self.balance}
        questions = [
            inquirer.List("card",
                          message="Which card would you like to buy?",
                          choices=list(card_name_to_class) + ["None!"])
        ]
        choice = inquirer.prompt(questions)["card"]
        if not choice == "None!":
            return card_name_to_class[choice]

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


def human_vs_computer(organism):
    game = Game(organism, Human())
    game.simulate()
    if game.winner == organism:
        print("You lost!")
    else:
        print("You won!")

