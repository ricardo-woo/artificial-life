import random
from organism import Organism
from Brain.Genome import Genome
from spatialgrid import SpatialGrid
from predator import Predator
from prey import Prey
from settings import (
    WORLD_WIDTH,
    WORLD_HEIGHT,
    SPATIAL_CELL_SIZE,
    REPRODUCTION_OFFSET,
    ELITE_CLONE_CHANCE,
    REPRODUCTION_ENERGY_COST,
    REPRODUCTION_INTERVAL,
    REPRODUCTION_CHILD_ENERGY,
    MAX_PREDATORS,
    MAX_PREY,
    PREDATOR_POPULATION_SIZE,
    PREY_POPULATION_SIZE,
    RESEED_COUNT,
    RESEED_DELAY,
)
import math

MAX_POPULATION_BY_SPECIES = {Predator: MAX_PREDATORS, Prey: MAX_PREY}


class Population:
    def __init__(self):
        self.organism_grid = SpatialGrid(SPATIAL_CELL_SIZE)

        self.best_genome = None
        self.best_fitness = float("-inf")

        self.extinct_time = {Predator: 0, Prey: 0}

    def update_organism_position(self, organism):
        self.organism_grid.update(organism, organism.x, organism.y)

    def find_best(self, organism):
        if organism.fitness > self.best_fitness:
            self.best_fitness = organism.fitness
            self.best_genome = organism.genome.copy()

    def record_death(self, organism):
        self.find_best(organism)

    def spawn_close(self, parent=Organism):
        angle = random.uniform(0, 2 * math.pi)

        offset_x = REPRODUCTION_OFFSET * random.uniform(0.5, 1.5)
        offset_y = REPRODUCTION_OFFSET * random.uniform(0.5, 1.5)

        x = parent.x + offset_x * math.cos(angle)
        y = parent.y + offset_y * math.sin(angle)

        x = max(0, min(WORLD_WIDTH, x))
        y = max(0, min(WORLD_HEIGHT, y))

        return x, y

    def reproduce(self, parent, organisms):
        self.find_best(parent)

        if random.random() < ELITE_CLONE_CHANCE:
            child_genome = parent.genome.copy()
        else:
            child_genome = parent.genome.copy()
            child_genome.mutate()

        parent.energy -= REPRODUCTION_ENERGY_COST
        parent.next_reproduction += REPRODUCTION_INTERVAL

        spawn_x, spawn_y = self.spawn_close(parent)

        species = type(parent)
        child = species(spawn_x, spawn_y, child_genome)
        child.energy = REPRODUCTION_CHILD_ENERGY

        same_species_living = [
            o
            for o in organisms
            if not o.is_dead() and o is not parent and type(o) is species
        ]

        max_species = MAX_POPULATION_BY_SPECIES[species]

        if len(same_species_living) >= max_species - 1:
            weakest = min(same_species_living, key=lambda o: o.fitness)
            self.record_death(weakest)
            self.organism_grid.remove(weakest)
            organisms.remove(weakest)

        organisms.append(child)
        self.organism_grid.insert(child, child.x, child.y)
        return child

    def update_extinctions(self, organisms, dt):
        for species in (Predator, Prey):
            alive = any(type(o) is species for o in organisms)

            if alive:
                self.extinct_time[species] = 0
                continue

            self.extinct_time[species] += dt

            if self.extinct_time[species] >= RESEED_DELAY:
                self.spawn_species(organisms, species, RESEED_COUNT)
                self.extinct_time[species] = 0

    def spawn_species(self, organisms, species, count):
        for _ in range(count):
            genome = Genome()
            organism = species(
                random.randint(0, WORLD_WIDTH), random.randint(0, WORLD_HEIGHT), genome
            )
            organisms.append(organism)
            self.organism_grid.insert(organism, organism.x, organism.y)

    def create_initial_population(self, organisms):
        self.organism_grid.clear()

        self.spawn_species(organisms, Prey, PREY_POPULATION_SIZE)
        self.spawn_species(organisms, Predator, PREDATOR_POPULATION_SIZE)
        return organisms
