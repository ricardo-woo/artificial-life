from organism import Organism
import math

from settings import MAX_ENERGY, PREDATOR_SPRITE, RAY_FOV_PREDATORS


class Predator(Organism):
    def __init__(self, x, y, genome):
        super().__init__(x, y, genome)

        self.type = "predator"

        self.image = PREDATOR_SPRITE

        self.ray_fov = RAY_FOV_PREDATORS

    def update(self, food_grid, organism_grid, dt):
        return super().update(food_grid, organism_grid, dt)

    def can_catch(self, prey):
        dx = prey.x - self.x
        dy = prey.y - self.y

        angle_to_prey = math.atan2(dy, dx)

        predator_alignment = math.cos(self.angle - angle_to_prey)

        prey_alignment = math.cos(prey.angle - angle_to_prey)

        return predator_alignment > 0.5 and prey_alignment > 0.3 and self.eat(prey)

    def eat_organism(self, target):
        if not self.can_catch(target):
            return False

        self.energy = min(MAX_ENERGY, self.energy + target.energy)
        target.energy = 0
        return True
