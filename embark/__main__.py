"""
__main__.py

@author Elliot Penson
"""

from crayons import magenta

from embark import evolution
from embark.play import human_vs_computer


def main():
    print(magenta("EMbArK: Evolutionary MAchi Koro", bold=True))
    winner = evolution.run()
    print("The most fit organism had the following chromosome:")
    evolution.print_organism(winner)
    if input("Would you like to play the best organism? [y/n] ") == "y":
        print()
        human_vs_computer(winner)

if __name__ == "__main__":
    main()
