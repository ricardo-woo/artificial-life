from organism import Organism

from settings import PREY_SPRITE, PREY_REPRODUCTION_AGE


class Prey(Organism):
    def __init__(self, x, y, genome):
        super().__init__(x, y, genome)

        self.type = "prey"

        self.image = PREY_SPRITE
        self.next_reproduction = PREY_REPRODUCTION_AGE

    def update(self, food_grid, organism_grid, dt):
        return super().update(food_grid, organism_grid, dt)
