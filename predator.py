from organism import Organism
import math

from settings import (
    MAX_ENERGY,
    PREDATOR_SPRITE,
    RAY_FOV_PREDATORS,
    PREDATOR_ATTACK_ANGLE,
)


class Predator(Organism):
    def __init__(self, x, y, genome):
        super().__init__(x, y, genome)

        self.type = "predator"

        self.image = PREDATOR_SPRITE

        self.ray_fov = RAY_FOV_PREDATORS

    def update(self, food_grid, organism_grid, dt):
        return super().update(food_grid, organism_grid, dt)

    def eat_organism(self, target):
        if not self.eat(target):
            return False

        dx = target.x - self.x
        dy = target.y - self.y

        angle_to_target = math.atan2(dy, dx)

        angle_difference = (angle_to_target - self.angle + math.pi) % (
            2 * math.pi
        ) - math.pi

        if abs(angle_difference) > PREDATOR_ATTACK_ANGLE:
            return False

        self.energy = min(MAX_ENERGY, self.energy + target.energy)
        target.energy = 0
        return True
