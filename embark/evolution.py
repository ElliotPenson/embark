"""
evolution.py

@author Elliot Penson
"""

from random import random, choice
from itertools import combinations
import csv

import numpy
from progress.bar import ChargingBar

from embark.machi_koro import Game, Player, ALL_CARDS
from embark.parameters import (NUMBER_OF_ROUNDS, GENERATION_SIZE, RECOMBINATION_PROBABILITY,
                               MUTATION_PROBABILITY, MUTATION_GAUSSIAN_WIDTH)


class Organism(Player):

    def __init__(self, chromosome):
        """Create an AI that plays Machi Koro by referencing a gene dictionary (card
        class -> probability of purchase).
        """
        self.chromosome = chromosome
        self.wins = 0
        
    def construct(self, available):
        """Sample from this player's genes to select and purchase a card."""
        relevant_genes = {card_class: probability
                          for card_class, probability in self.chromosome.items()
                          if card_class in available}
        return select_card(relevant_genes)

    def __getitem__(self, card):
        return self.chromosome[card]

    def __setitem__(self, card, probability):
        self.chromosome[card] = probability

    def get_genes(self):
        return self.chromosome.keys()


def run():
    print(f"Performing evolution with {GENERATION_SIZE} organisms for {NUMBER_OF_ROUNDS} rounds.")
    generation = {Organism(make_random_chromosome()) for _ in range(GENERATION_SIZE)}
    for _ in ChargingBar("Iterating").iter(list(range(NUMBER_OF_ROUNDS))):
        generation = set(iterate(generation))
    return max(generation, key=lambda organism: organism.wins)


def iterate(generation):
    """Form a new generation from an old generation. Choose parents by fitness-proportionate
    selection.

    :param generation: List of Organisms
    """
    set_fitness(generation)
    total_fitness = sum(organism.wins for organism in generation)
    weights = {organism: organism.wins / total_fitness for organism in generation}
    for _ in range(GENERATION_SIZE):
        parent1, parent2 = sample_by_probability(weights, 2)
        child = breed(parent1, parent2)
        if random() < MUTATION_PROBABILITY:
            mutate(child)
        yield child


def breed(parent1, parent2):
    """Use uniform crossover to produce a child from two parent organisms."""
    chromosome = {card: parent1[card] if random() < RECOMBINATION_PROBABILITY else parent2[card]
                  for card in ALL_CARDS}
    return Organism(chromosome)


def mutate(organism):
    """Add noise from a Gaussian random variable to a chosen gene."""
    genes = organism.get_genes()
    for card in genes:
        if random() < 1 / len(genes):
            # Mutate one gene on average.
            organism[card] += numpy.random.normal(0, MUTATION_GAUSSIAN_WIDTH)

            # Ensure 0 <= probability <= 1.
            if organism[card] > 1:
                organism[card] = 1
            elif organism[card] < 0:
                organism[card] = 0


def set_fitness(generation):
    """Simulate Machi Koro games to find a win rate for a list of Organisms."""
    for player in generation:
        player.wins = 0  # Reset win rates.
    for player1, player2 in combinations(generation, 2):
        game = Game(player1, player2)
        game.simulate()
        if game.winner == player1:
            player1.wins += 1
        else:
            player2.wins += 1


def select_card(chromosome):
    """Choose a card by referencing a strategy. The genes parameter is a dictionary from card class
    -> probability of selection.
    """
    if sum(chromosome.values()) == 0:
        return choice(list(chromosome))  # Choose an arbitrary card.

    chromosome = normalize(chromosome)
    return sample_by_probability(chromosome)


def sample_by_probability(probability_dict, n_samples=None):
    """Randomly choose a key from a dict by the weight of its value. The sum of dict values should
    equal one.
    """
    return numpy.random.choice(list(probability_dict.keys()),
                               size=n_samples,
                               p=list(probability_dict.values()))


def normalize(chromosome):
    """Make all probabilities sum to one."""
    total = sum(chromosome.values())
    return {card: probability / total for card, probability in chromosome.items()}


def make_random_chromosome():
    chromosome = {card: random() for card in ALL_CARDS}
    return normalize(chromosome)


def print_organism(self, bar_width=100):
    """Print the genes of an organism as a horizontal bar chart."""
    solid_block = u"\u2588"

    longest_length = max(len(card.__name__) for card in self.chromosome)
    def pad(card_name):
        return card_name + " " * (longest_length - len(card_name))

    for card, probability in self.chromosome.items():
        print(f"{pad(card.__name__)} {solid_block * int(probability * bar_width)}")


def export(generation, file_name="report.csv"):
    with open(file_name, "w", newline="") as csvfile:
        report = csv.writer(csvfile)
        # Create heading.
        report.writerow(["Wins"] + [card.__name__ for card in ALL_CARDS])
        for organism in generation:
            report.writerow([organism.wins] + [organism[card] for card in ALL_CARDS])
