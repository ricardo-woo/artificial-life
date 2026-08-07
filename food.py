import pygame

from settings import FOOD_COLOR,FOOD_RADIUS


class Food:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.radius = FOOD_RADIUS

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
            FOOD_COLOR,
            (screen_x, screen_y),
            radius
        )
