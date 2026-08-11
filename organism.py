import pygame
import math
import random
import time

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
    SELECTION_CLICK_PADDING,
    WALK_SPEED_COEFFICIENT,
    RUN_SPEED_COEFFICIENT,
    NUM_RAYS,
    RAY_CATEGORIES,
    REPRODUCTION_ENERGY_COST,
    REPRODUCTION_AGE,
)
from noise import OU_Noise


def distance_to_world_bounds(x, y, dx, dy, angle, max_length):
    t = max_length

    if dx > 0:
        t = min(t, (WORLD_WIDTH - x) / dx)
    elif dx < 0:
        t = min(t, (0 - x) / dx)

    if dy > 0:
        t = min(t, (WORLD_HEIGHT - y) / dy)
    elif dy < 0:
        t = min(t, (0 - y) / dy)

    return max(0, t)


def cast_ray(x, y, angle, max_length, food_candidates, organism_candidates, organism):
    dx, dy = math.cos(angle), math.sin(angle)
    wall_t = distance_to_world_bounds(x, y, dx, dy, angle, max_length)

    closest_t = wall_t
    closest_category = "obstacle" if wall_t < max_length else None

    if food_candidates:

        for obj in food_candidates:
            obj_dx, obj_dy = obj.x - x, obj.y - y

            proj = obj_dx * dx + obj_dy * dy
            if proj < 0 or proj > closest_t:
                continue

            closest_x, closest_y = x + dx * proj, y + dy * proj
            center_dist = math.hypot(obj.x - closest_x, obj.y - closest_y)

            if center_dist > obj.radius:
                continue

            offset = math.sqrt(obj.radius**2 - center_dist**2)
            t = proj - offset

            if 0 <= t < closest_t:
                closest_t = t
                closest_category = "food"

    for obj in organism_candidates:

        if obj is organism:
            continue

        obj_dx, obj_dy = obj.x - x, obj.y - y

        proj = obj_dx * dx + obj_dy * dy
        if proj < 0 or proj > closest_t:
            continue

        closest_x, closest_y = x + dx * proj, y + dy * proj
        center_dist = math.hypot(obj.x - closest_x, obj.y - closest_y)

        if center_dist > obj.radius:
            continue

        offset = math.sqrt(obj.radius**2 - center_dist**2)
        t = proj - offset

        if 0 <= t < closest_t:
            closest_t = t
            closest_category = obj.type

    return closest_t, closest_category


def ray_to_input(distance, category, max_length):
    distance_normalized = distance / max_length
    one_hot = [0] * len(RAY_CATEGORIES)
    if category is not None:
        one_hot[RAY_CATEGORIES.index(category)] = 1
    return [distance_normalized] + one_hot


class Organism:

    def get_data(self):

        return {
            "type": self.type,
            "x": self.x,
            "y": self.y,
            "energy": self.energy,
            "age": self.age,
            "food_eaten": self.food_eaten,
            "angle": self.angle,
            "genome": self.genome.get_data(),
            "next_reproduction": self.next_reproduction,
        }

    @property
    def fitness(self):
        return (
            self.food_eaten * FITNESS_FOOD_WEIGHT
            + min(self.age, FITNESS_AGE_CAP) / FITNESS_AGE_DIVISOR
        )

    def __init__(self, x, y, genome):
        self.type = "organism"

        # Genome
        self.genome = genome

        # Physical properties
        self.radius = genome.radius
        self.speed = genome.speed
        self.max_turn_speed = genome.max_turn_speed
        self.vision = genome.vision
        self.ray_fov = math.radians(200)

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
        self.rays = []
        self.brain_inputs = []
        self.brain_outputs = []

        # Sprite
        self.image = None

        # Reproduction
        self.next_reproduction = REPRODUCTION_AGE

    # UPDATE

    def update(self, food_grid, organism_grid, dt):
        self.age += dt
        self.time_since_food += dt

        self.energy -= BASE_ENERGY_DECAY * dt
        self.energy -= (self.vision * VISION_ENERGY_COST) * dt
        self.energy -= self.radius * RADIUS_ENERGY_COST * dt

        self.current_noise = self.wandering_noise.step(dt)

        self.brain_inputs = self.get_brain_inputs(food_grid, organism_grid)

        self.brain_outputs = self.brain.predict(self.brain_inputs)

        turn = self.brain_outputs[0]
        movement = (self.brain_outputs[1] + 1) / 2

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

    def ready_to_reproduce(self):
        return (
            self.age >= self.next_reproduction
            and self.energy >= REPRODUCTION_ENERGY_COST
        )

    # SENSORS

    def cast_rays(self, food_grid, organism_grid):
        half_fov = self.ray_fov / 2
        rays = []

        nearby_organisms = organism_grid.query(self.x, self.y, self.vision)

        nearby_food = None

        if not self.type == "predator":
            nearby_food = food_grid.query(self.x, self.y, self.vision)

        for i in range(NUM_RAYS):
            if NUM_RAYS == 1:
                offset = 0
            else:
                offset = -half_fov + (self.ray_fov * i / (NUM_RAYS - 1))

            ray_angle = self.angle + offset
            distance, category = cast_ray(
                self.x,
                self.y,
                ray_angle,
                self.vision,
                nearby_food,
                nearby_organisms,
                self,
            )

            rays.append(
                {
                    "angle": ray_angle,
                    "distance": distance,
                    "category": category,
                    "input": ray_to_input(distance, category, self.vision),
                }
            )

        return rays

    def get_brain_inputs(self, food_grid, organism_grid):
        self.rays = self.cast_rays(food_grid, organism_grid)

        ray_inputs = [r["input"] for r in self.rays]
        ray_summaries = self.ray_sensor.process(ray_inputs)

        ray_inputs_flat = [value for ray in ray_summaries for value in ray]

        target_visible = any(r["category"] == "food" for r in self.rays)

        if self.type == "predator":

            target_visible = any(r["category"] == "prey" for r in self.rays)

        gated_noise = 0 if target_visible else self.current_noise

        global_inputs = [
            self.energy / MAX_ENERGY,
            min(self.time_since_food / 100, 1),
            gated_noise,
        ]

        return ray_inputs_flat + global_inputs

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
        if self.is_dead():
            return

        screen_x, screen_y = camera.world_to_screen(self.x, self.y)

        radius = max(1, int(self.radius * camera.zoom))

        scale = camera.zoom

        image = pygame.transform.scale(
            self.image,
            (
                int(self.image.get_width() * scale),
                int(self.image.get_height() * scale),
            ),
        )

        angle_degrees = -math.degrees(self.angle) - 90

        image = pygame.transform.rotate(image, angle_degrees)

        rect = image.get_rect(center=(screen_x, screen_y))
        screen.blit(image, rect)

    def draw_rays(self, screen, camera):
        rays = self.rays

        origin_x, origin_y = camera.world_to_screen(self.x, self.y)

        for ray in rays:
            end_x = self.x + math.cos(ray["angle"]) * ray["distance"]
            end_y = self.y + math.sin(ray["angle"]) * ray["distance"]
            screen_end_x, screen_end_y = camera.world_to_screen(end_x, end_y)

            if ray["category"] == "food":
                color = (80, 220, 80)
            elif ray["category"] == "obstacle":
                color = (255, 255, 0)
            elif ray["category"] == "prey":
                color = (48, 92, 222)
            elif ray["category"] == "predator":
                color = (255, 0, 56)
            else:
                color = (140, 140, 140)

            pygame.draw.line(
                screen,
                color,
                (origin_x, origin_y),
                (screen_end_x, screen_end_y),
                1,
            )

            if ray["category"] is not None:
                pygame.draw.circle(screen, color, (screen_end_x, screen_end_y), 4)
