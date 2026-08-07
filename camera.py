import pygame

from settings import WIDTH, HEIGHT, DEFAULT_ZOOM, ZOOM_FACTOR, MAX_ZOOM, MIN_ZOOM


class Camera:

    def __init__(self):
        self.x = 0
        self.y = 0

        self.zoom = DEFAULT_ZOOM

        self.dragging = False
        self.last_mouse_pos = None

        self.following = None

    def world_to_screen(self, world_x, world_y):

        screen_x = (world_x - self.x) * self.zoom
        screen_y = (world_y - self.y) * self.zoom

        return int(screen_x), int(screen_y)

    def screen_to_world(self, screen_x, screen_y):

        world_x = screen_x / self.zoom + self.x
        world_y = screen_y / self.zoom + self.y

        return world_x, world_y

    def update(self):

        if self.following is not None:

            # Keep the followed organism in the center
            self.x = (
                self.following.x
                - WIDTH / (2 * self.zoom)
            )

            self.y = (
                self.following.y
                - HEIGHT / (2 * self.zoom)
            )

    def start_drag(self):

        self.dragging = True
        self.last_mouse_pos = pygame.mouse.get_pos()

    def stop_drag(self):

        self.dragging = False
        self.last_mouse_pos = None

    def drag(self):

        if not self.dragging:
            return

        mouse_x, mouse_y = pygame.mouse.get_pos()

        last_x, last_y = self.last_mouse_pos

        dx = mouse_x - last_x
        dy = mouse_y - last_y

        self.x -= dx / self.zoom
        self.y -= dy / self.zoom

        self.last_mouse_pos = (
            mouse_x,
            mouse_y
        )

    def zoom_in(self):

        self.zoom *= ZOOM_FACTOR
        self.zoom = min(self.zoom, MAX_ZOOM)

    def zoom_out(self):

        self.zoom /= ZOOM_FACTOR
        self.zoom = max(self.zoom, MIN_ZOOM)
