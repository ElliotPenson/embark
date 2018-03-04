"""
parameters.py

@author Elliot Penson
"""

NUMBER_OF_ROUNDS = 1000
GENERATION_SIZE = 100

# Chance that a gene comes from one parent versus the other.
RECOMBINATION_PROBABILITY = 0.5

# Probability that an individual will experience mutation.
MUTATION_PROBABILITY = 0.25

# The standard deviation the Gaussian distributed used to mutate a single gene.
MUTATION_GAUSSIAN_WIDTH = 0.01
