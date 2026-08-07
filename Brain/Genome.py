import random

from Brain.NeuralNetwork import NeuralNetwork
from settings import (
    MIN_SPEED, MAX_SPEED, MIN_VISION, MAX_VISION,
    MAX_RADIUS, MIN_RADIUS, MAX_TURN_SPEED, MIN_TURN_SPEED,
    MUTATE_RADIUS_STEP, MUTATE_SPEED_STEP, MUTATE_TURN_SPEED_STEP,
    MUTATE_VISION_STEP
)

class Genome:
    def __init__(self):
        self.speed = random.uniform(MIN_SPEED, MAX_SPEED)
        self.max_turn_speed = random.uniform(MIN_TURN_SPEED, MAX_TURN_SPEED)
        self.vision = random.uniform(MIN_VISION, MAX_VISION)
        self.radius = random.uniform(MIN_RADIUS, MAX_RADIUS)
        self.brain = NeuralNetwork()

    def copy(self):

        child = Genome()

        child.speed = self.speed
        child.max_turn_speed = self.max_turn_speed
        child.vision = self.vision
        child.radius = self.radius

        child.brain = self.brain.copy()

        return child

    def mutate(self):
        self.speed += random.uniform(-MUTATE_SPEED_STEP, MUTATE_SPEED_STEP)
        self.speed = max(MIN_SPEED, min(MAX_SPEED, self.speed))

        self.vision += random.uniform(-MUTATE_VISION_STEP, MUTATE_VISION_STEP)
        self.vision = max(MIN_VISION, min(MAX_VISION, self.vision))

        self.radius += random.uniform(-MUTATE_RADIUS_STEP, MUTATE_RADIUS_STEP)
        self.radius = max(MIN_RADIUS, min(MAX_RADIUS, self.radius))

        self.max_turn_speed += random.uniform(-MUTATE_TURN_SPEED_STEP, MUTATE_TURN_SPEED_STEP)
        self.max_turn_speed = max(
            MIN_TURN_SPEED, min(MAX_TURN_SPEED, self.max_turn_speed)
        )

        self.brain.mutate()

    def get_data(self):

        return {
            "speed": self.speed,
            "max_turn_speed": self.max_turn_speed,
            "vision": self.vision,
            "radius": self.radius,
            "brain": self.brain.get_data(),
        }

    @staticmethod
    def from_data(data):

        genome = Genome()

        genome.speed = data["speed"]

        genome.max_turn_speed = data["max_turn_speed"]

        genome.vision = data["vision"]

        genome.radius = data["radius"]

        genome.brain = NeuralNetwork.from_data(data["brain"])

        return genome
