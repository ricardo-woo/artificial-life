import pygame

from settings import BUSH_IMAGE


class Bush:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = BUSH_IMAGE

    def draw(self, screen, camera):
        screen_x, screen_y = camera.world_to_screen(self.x, self.y)

        image = pygame.transform.scale(self.image,(int(self.image.get_width() * camera.zoom),int(self.image.get_height() * camera.zoom),))

        rect = image.get_rect(center=(screen_x, screen_y))
        screen.blit(image, rect)