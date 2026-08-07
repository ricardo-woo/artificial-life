import random

from Brain.NeuralNetwork import NeuralNetwork

# SPEED
MIN_SPEED = 0.1
MAX_SPEED = 4

# VISION
MIN_VISION = 80
MAX_VISION = 300

# RADIUS
MIN_RADIUS = 10
MAX_RADIUS = 15

# TURN SPEED
MIN_TURN_SPEED = 0.01
MAX_TURN_SPEED = 2


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
        self.speed += random.uniform(-0.1, 0.1)
        self.speed = max(MIN_SPEED, min(MAX_SPEED, self.speed))

        self.vision += random.uniform(-5, 5)
        self.vision = max(MIN_VISION, min(MAX_VISION, self.vision))

        self.radius += random.uniform(-0.5, 0.5)
        self.radius = max(MIN_RADIUS, min(MAX_RADIUS, self.radius))

        self.max_turn_speed += random.uniform(-0.05, 0.05)
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
