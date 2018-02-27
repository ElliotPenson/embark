"""
evolution.py

@author Elliot Penson
"""

from random import random, choice
from itertools import combinations

from numpy.random import normal

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


def main():
    generation = {Organism(make_random_chromosome()) for _ in range(GENERATION_SIZE)}
    for _ in range(NUMBER_OF_ROUNDS):
        generation = set(iterate(generation))
    return generation


def iterate(generation):
    """Form a new generation from an old generation. Choose parents by fitness-proportionate
    selection.

    :param generation: List of Organisms
    """
    set_fitness(generation)
    total_fitness = sum(organism.wins for organism in generation)
    weights = {organism: organism.wins / total_fitness for organism in generation}
    for _ in range(GENERATION_SIZE):
        # TODO make sure there's no asexual reproduction
        parent1 = select_by_probability(weights)
        parent2 = select_by_probability(weights)
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
            organism[card] += normal(0, MUTATION_GAUSSIAN_WIDTH)

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
        return choice(chromosome)  # Choose an arbitrary card.

    chromosome = normalize(chromosome)
    return select_by_probability(chromosome)


def select_by_probability(probability_dict):
    """Randomly choose a key from a dict by weight of its value. The sum of dict values should
    equal one.
    """
    running_total = 0
    sample = random()
    for item in probability_dict:
        running_total += probability_dict[item]
        if running_total >= sample:
            return item


def normalize(chromosome):
    """Make all probabilities sum to one."""
    total = sum(chromosome.values())
    return {card: probability / total for card, probability in chromosome.items()}


def make_random_chromosome():
    chromosome = {card: random() for card in ALL_CARDS}
    return normalize(chromosome)
