from organism import Organism

from settings import MAX_ENERGY


class Predator(Organism):
    def __init__(self, x, y, genome):
        super().__init__(x, y, genome)

        self.type = "predator"

        self.kills = 0

    def update(self, food_grid, organism_grid, dt):
        return super().update(food_grid, organism_grid, dt)

    def eat_organism(self, target):
        if self.eat(target):
            self.energy = min(MAX_ENERGY, self.energy + target.energy * 0.5)
            self.kills += 1
            target.energy = 0
            return True
        return False
