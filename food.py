import pygame
import random
import math

from settings import (
    FOOD_COLOR,
    FOOD_RADIUS,
    WORLD_HEIGHT,
    WORLD_WIDTH,
    FOOD_BUSH_RADIUS,
    ORB_FOOD_SPRITE,
)


class Food:

    def __init__(self, bushes):

        bush = random.choice(bushes)

        angle = random.uniform(0, math.tau)
        distance = random.uniform(50, FOOD_BUSH_RADIUS)

        x = bush.x + math.cos(angle) * distance
        y = bush.y + math.sin(angle) * distance

        x = max(0, min(WORLD_WIDTH, x))
        y = max(0, min(WORLD_HEIGHT, y))

        self.x = x
        self.y = y

        self.radius = FOOD_RADIUS

        self.image = ORB_FOOD_SPRITE

    def draw(self, screen, camera):
        screen_x, screen_y = camera.world_to_screen(self.x, self.y)

        scale = camera.zoom / 3

        image = pygame.transform.scale(
            self.image,
            (
                int(self.image.get_width() * scale),
                int(self.image.get_height() * scale),
            ),
        )

        rect = image.get_rect(center=(screen_x, screen_y))
        screen.blit(image, rect)
