"""
__main__.py

@author Elliot Penson
"""

from crayons import magenta

from embark import evolution


if __name__ == "__main__":
    print(magenta('EMbArK: Evolutionary MAchi Koro', bold=True))
    evolution.main()
