# EMbArK: Evolutionary MAchi Koro

[![Build Status](https://travis-ci.org/ElliotPenson/embark.svg?branch=master)](https://travis-ci.org/ElliotPenson/embark)

An engine for the Japanese game Machi Koro with a genetic algorithm to generate
AI.

## What is Machi Koro?

![Machi Koro Logo](http://idwgames.com/wp-content/uploads/2014/09/machi-koro.jpg)

Machi Koro is a fun, card-based board game. Each turn, the current player rolls
the dice, earns coins, and purchases one card. The first player to build all
four landmark cards wins the game.

## Execution

```
virtualenv venv                  # Create a virtual environment.
. venv/bin/activate              # Activate the virtual environment.
pip install -r requirements.pip  # Install dependencies.
python -m embark                 # Run embark.
```

Algorithm parameters may be adjusted in `embark/parameters.py`.
