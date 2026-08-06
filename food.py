import pygame

from settings import WORLD_WIDTH, WORLD_HEIGHT


class Food:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.radius = 4

    def draw(self, screen, camera):

        screen_x, screen_y = camera.world_to_screen(
            self.x,
            self.y
        )

        radius = max(
            1,
            int(self.radius * camera.zoom)
        )

        pygame.draw.circle(
            screen,
            (220, 200, 80),
            (screen_x, screen_y),
            radius
        )
