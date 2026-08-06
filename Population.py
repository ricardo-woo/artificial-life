import random
from organism import Organism
from Brain.Genome import Genome
from settings import WORLD_WIDTH, WORLD_HEIGHT

POPULATION_SIZE = 100
PARENT_COUNT = 5


class Population:
    def __init__(self):
        pass

    def next_generation(self, organisms):
        organisms.sort(key=lambda organism: organism.fitness, reverse=True)

        parents = organisms[:PARENT_COUNT]

        children = []

        best_parent = organisms[0]

        elite_genome = best_parent.genome.copy()

        elite_x = random.randint(0, WORLD_WIDTH)
        elite_y = random.randint(0, WORLD_HEIGHT)

        elite_child = Organism(elite_x, elite_y, elite_genome)

        children.append(elite_child)

        while len(children) < POPULATION_SIZE:
            parent = random.choice(parents)

            genome = parent.genome.copy()

            genome.mutate()

            random_x = random.randint(0, WORLD_WIDTH)
            random_y = random.randint(0, WORLD_HEIGHT)

            child = Organism(random_x, random_y, genome)

            children.append(child)
        return children

    def create_initial_population(self, organisms):
        for _ in range(100):
            genome = Genome()
            organism = Organism(
                random.randint(0, WORLD_WIDTH), random.randint(0, WORLD_HEIGHT), genome
            )
            organisms.append(organism)
        return organisms
