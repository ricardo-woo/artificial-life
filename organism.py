import pygame
import math
import random

from settings import (
    WORLD_WIDTH,
    WORLD_HEIGHT,
    MAX_ENERGY,
    BASE_ENERGY_DECAY,
    VISION_ENERGY_COST,
    RADIUS_ENERGY_COST,
    WALK_RUN_TRANSITION,
    IDLE_ENERGY_TAX,
    IDLE_VELOCITY_TRESHOLD,
    FITNESS_AGE_CAP,
    FITNESS_AGE_DIVISOR,
    FITNESS_FOOD_WEIGHT,
    NOISE_MU,
    NOISE_SIGMA,
    NOISE_THETA,
    ORGANISM_COLOR,
    SELECTION_CLICK_PADDING,
    WALK_SPEED_COEFFICIENT,
    RUN_SPEED_COEFFICIENT,
    NUM_RAYS,
    RAY_CATEGORIES,
    RAY_FOV,
)
from noise import OU_Noise


def cast_ray(x, y, angle, max_length, food_grid):
    dx, dy = math.cos(angle), math.sin(angle)

    closest = max_length
    closest_type = None

    candidates = food_grid.query(x, y, max_length)

    for candidate in candidates:
        candidate_dx, candidate_dy = candidate.x - x, candidate.y - y

        projection = candidate_dx * dx + candidate_dy * dy
        if projection < 0 or projection > closest:
            continue

        closest_x, closest_y = x + dx * projection, y + dy * projection
        center_distance = math.dist([candidate.x, candidate.y], [closest.x, closest.y])

        if center_distance > candidate.radius:
            continue

        offset = math.sqrt(candidate.radius**2 - center_distance**2)
        t = projection - offset

        if 0 <= t < closest:
            closest = t
            closest_type = "food"

    return closest, closest_type


def ray_to_input(distance, category, max_length):
    distance_normalized = distance / max_length
    one_hot = [0] * len[RAY_CATEGORIES]
    if category is not None:
        one_hot[RAY_CATEGORIES.index(category)] = 1
    return [distance_normalized] + one_hot


class Organism:

    def get_data(self):

        return {
            "x": self.x,
            "y": self.y,
            "energy": self.energy,
            "age": self.age,
            "food_eaten": self.food_eaten,
            "angle": self.angle,
            "genome": self.genome.get_data(),
        }

    @property
    def fitness(self):
        return (
            self.food_eaten * FITNESS_FOOD_WEIGHT
            + min(self.age, FITNESS_AGE_CAP) / FITNESS_AGE_DIVISOR
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
        self.wandering_noise = OU_Noise(
            mu=NOISE_MU, theta=NOISE_THETA, sigma=NOISE_SIGMA
        )
        self.current_noise = 0
        # Position
        self.x = x
        self.y = y

        # Score
        self.food_eaten = 0
        self.age = 0

        # Survival
        self.energy = MAX_ENERGY
        self.time_since_food = 0

        # Exploration tracking
        self.idle_time = 0

        # Movement
        self.angle = random.uniform(0, math.tau)

        # Brain
        self.brain = genome.brain
        self.ray_sensor = genome.ray_sensor

    # UPDATE

    def update(self, food_grid, dt):
        self.age += dt
        self.time_since_food += dt

        self.energy -= BASE_ENERGY_DECAY * dt
        self.energy -= (self.vision * VISION_ENERGY_COST) * dt
        self.energy -= self.radius * RADIUS_ENERGY_COST * dt

        self.current_noise = self.wandering_noise.step(dt)

        inputs = self.get_brain_inputs(food_grid)
        outputs = self.brain.predict(inputs)

        turn = outputs[0]
        movement = (outputs[1] + 1) / 2

        actual_speed = movement * self.speed

        if actual_speed >= WALK_RUN_TRANSITION:
            movement_cost = RUN_SPEED_COEFFICIENT * actual_speed * dt
        else:
            movement_cost = WALK_SPEED_COEFFICIENT * actual_speed * dt

        self.energy -= movement_cost

        self.angle += turn * self.max_turn_speed * dt
        self.angle %= math.tau

        old_x, old_y = self.x, self.y

        self.x += math.cos(self.angle) * self.speed * movement * dt
        self.y += math.sin(self.angle) * self.speed * movement * dt

        self.keep_inside_world()

        frame_distance = math.hypot(self.x - old_x, self.y - old_y)

        velocity = frame_distance / dt if dt > 0 else 0

        if velocity < IDLE_VELOCITY_TRESHOLD:
            self.idle_time += dt
            self.energy -= IDLE_ENERGY_TAX * dt
        else:
            self.idle_time = 0

    # SENSORS

    def cast_rays(self, food_grid):

        half_fov = RAY_FOV / 2
        rays = []

        for i in range(NUM_RAYS):
            if NUM_RAYS == 1:
                offset = 0
            else:
                offset = -half_fov + (RAY_FOV * i / (NUM_RAYS - 1))

            ray_angle = self.angle + offset
            distance, category = cast_ray(
                self.x, self.y, ray_angle, self.vision, food_grid
            )
            rays.append((ray_to_input(distance, category, self.vision), category))

        return rays

    def get_brain_inputs(self, food_grid):
        rays = self.cast_rays(food_grid)

        ray_inputs = [r[0] for r in rays]

        ray_summaries = self.ray_sensor.process(ray_inputs)

        food_visible = any(category == "food" for _, category in rays)

        gated_noise = 0 if food_visible else self.current_noise

        inputs = [
            self.energy / MAX_ENERGY,
            min(self.time_since_food / 100, 1),
            gated_noise,
        ]

        return ray_summaries + inputs

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

        return distance <= self.radius + SELECTION_CLICK_PADDING

    def draw(self, screen, camera):

        screen_x, screen_y = camera.world_to_screen(self.x, self.y)

        radius = max(1, int(self.radius * camera.zoom))

        pygame.draw.circle(screen, ORGANISM_COLOR, (screen_x, screen_y), radius)
