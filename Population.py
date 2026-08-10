import random
from organism import Organism
from Brain.Genome import Genome
from spatialgrid import SpatialGrid
from settings import (
    WORLD_WIDTH,
    WORLD_HEIGHT,
    POPULATION_SIZE,
    PARENT_COUNT,
    SPATIAL_CELL_SIZE,
)


class Population:
    def __init__(self):
        self.organism_grid = SpatialGrid(SPATIAL_CELL_SIZE)

    def update_organism_position(self, organism):
        self.organism_grid.update(organism, organism.x, organism.y)

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
        self.organism_grid.clear()
        self.organism_grid.insert(elite_child, elite_child.x, elite_child.y)

        while len(children) < POPULATION_SIZE:
            parent = random.choice(parents)

            genome = parent.genome.copy()

            genome.mutate()

            random_x = random.randint(0, WORLD_WIDTH)
            random_y = random.randint(0, WORLD_HEIGHT)

            child = Organism(random_x, random_y, genome)

            children.append(child)
            self.organism_grid.insert(child, child.x, child.y)
        return children

    def create_initial_population(self, organisms):
        self.organism_grid.clear()

        for _ in range(POPULATION_SIZE):
            genome = Genome()
            organism = Organism(
                random.randint(0, WORLD_WIDTH), random.randint(0, WORLD_HEIGHT), genome
            )
            organisms.append(organism)
            self.organism_grid.insert(organism, organism.x, organism.y)
        return organisms
