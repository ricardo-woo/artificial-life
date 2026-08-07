import pygame
import math
import random

from settings import WORLD_WIDTH, WORLD_HEIGHT
from noise import OU_Noise

# Below this ACTUAL velocity (world units per simulated second), the
# organism counts as idle. This is deliberately based on measured
# displacement, not the raw brain "movement" output — checking the raw
# output let a genome evolve a tiny `speed` so a movement output near 1.0
# still barely moves it, dodging the tax entirely. Tying it to real
# velocity (speed * movement) closes that loophole: a slow genome must
# commit to near-max output to clear the bar, and can't fake it.
IDLE_VELOCITY_THRESHOLD = 0.2

# Extra energy drained per second while idle, on top of normal upkeep.
IDLE_ENERGY_TAX = 0.05

# Fitness points earned per world-unit of path length traveled.
DISTANCE_FITNESS_WEIGHT = 0.02


class Organism:

    def get_data(self):

        return {
            "x": self.x,
            "y": self.y,
            "energy": self.energy,
            "age": self.age,
            "food_eaten": self.food_eaten,
            "angle": self.angle,
            "distance_traveled": self.distance_traveled,
            "genome": self.genome.get_data(),
        }

    @property
    def fitness(self):
        return (
            self.food_eaten * 10
            + min(self.age, 500) / 100
            + self.distance_traveled * DISTANCE_FITNESS_WEIGHT
        )

    def __init__(self, x, y, genome):
        # Genome
        self.genome = genome

        # Physical properties
        self.radius = genome.radius
        self.speed = genome.speed
        self.max_turn_speed = genome.max_turn_speed
        self.vision = genome.vision

        # Exploration
        self.wandering_noise = OU_Noise(mu=0.0, theta=0.5, sigma=0.8)
        self.current_noise = 0
        # Position
        self.x = x
        self.y = y

        # Score
        self.food_eaten = 0
        self.age = 0

        # Survival
        self.energy = 100
        self.time_since_food = 0

        # Exploration tracking
        self.distance_traveled = 0
        self.idle_time = 0

        # Movement
        self.angle = random.uniform(0, math.tau)

        # Brain
        self.brain = genome.brain

    # UPDATE

    def update(self, foods, dt):
        self.age += dt
        self.time_since_food += dt

        self.energy -= 0.1 * dt
        self.energy -= (self.vision * 0.0005) * dt
        self.energy -= self.radius * 0.001 * dt

        self.current_noise = self.wandering_noise.step(dt)

        inputs = self.get_brain_inputs(foods)
        outputs = self.brain.predict(inputs)

        turn = outputs[0]
        movement = (outputs[1] + 1) / 2

        self.energy -= (movement * self.speed * 0.01) * dt

        self.angle += turn * self.max_turn_speed * dt
        self.angle %= math.tau

        old_x, old_y = self.x, self.y

        self.x += math.cos(self.angle) * self.speed * movement * dt
        self.y += math.sin(self.angle) * self.speed * movement * dt

        self.keep_inside_world()

        frame_distance = math.hypot(self.x - old_x, self.y - old_y)
        self.distance_traveled += frame_distance

        velocity = frame_distance / dt if dt > 0 else 0

        if velocity < IDLE_VELOCITY_THRESHOLD:
            self.idle_time += dt
            self.energy -= IDLE_ENERGY_TAX * dt
        else:
            self.idle_time = 0

    # SENSORS

    def get_brain_inputs(self, foods):
        closest_food = None
        closest_distance = self.vision

        for food in foods:

            distance = math.sqrt((self.x - food.x) ** 2 + (self.y - food.y) ** 2)

            if distance < closest_distance and distance <= self.vision:
                closest_distance = distance
                closest_food = food

        if closest_food is not None:  # Calculate angle to closest food

            direction_x = closest_food.x - self.x
            direction_y = closest_food.y - self.y

            angle_to_food = math.atan2(direction_y, direction_x)
            angle_difference = angle_to_food - self.angle

            return [
                self.energy / 100,
                1,
                closest_distance / self.vision,
                math.sin(angle_difference),
                math.cos(angle_difference),
                min(self.time_since_food / 100, 1),
                self.current_noise,
            ]

        else:
            return self.no_food_in_vision()

    def no_food_in_vision(self):
        return [
            self.energy / 100,
            0,
            1,
            0,
            0,
            min(self.time_since_food / 100, 1),
            self.current_noise,
        ]

    # FOOD

    def eat(self, food):

        distance = math.sqrt((self.x - food.x) ** 2 + (self.y - food.y) ** 2)

        return distance <= self.radius + food.radius

    # WORLD BOUNDARIES

    def keep_inside_world(self):

        self.x = max(self.radius, min(WORLD_WIDTH - self.radius, self.x))

        self.y = max(self.radius, min(WORLD_HEIGHT - self.radius, self.y))

    def is_dead(self):

        return self.energy <= 0

    def contains_point(self, x, y):

        distance = math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)

        return distance <= self.radius + 5

    def draw(self, screen, camera):

        screen_x, screen_y = camera.world_to_screen(self.x, self.y)

        radius = max(1, int(self.radius * camera.zoom))

        pygame.draw.circle(screen, (100, 220, 100), (screen_x, screen_y), radius)
