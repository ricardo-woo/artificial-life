import math
import random


def poisson_disk_sampling(width, height, min_distance, k=30, rng=None):

    if min_distance <= 0:
        raise ValueError("min_distance must be positive")

    rng = rng or random

    cell_size = min_distance / math.sqrt(2)
    grid_width = max(1, int(math.ceil(width / cell_size)))
    grid_height = max(1, int(math.ceil(height / cell_size)))
    grid = [None] * (grid_width * grid_height)

    def grid_coords(x, y):
        return int(x / cell_size), int(y / cell_size)

    def fits(x, y):
        if not (0 <= x < width and 0 <= y < height):
            return False

        gx, gy = grid_coords(x, y)

        for ix in range(max(gx - 2, 0), min(gx + 3, grid_width)):
            for iy in range(max(gy - 2, 0), min(gy + 3, grid_height)):
                neighbor = grid[iy * grid_width + ix]
                if neighbor is not None:
                    nx, ny = neighbor
                    if math.hypot(nx - x, ny - y) < min_distance:
                        return False
        return True

    def place(x, y):
        gx, gy = grid_coords(x, y)
        grid[gy * grid_width + gx] = (x, y)
        points.append((x, y))
        active.append((x, y))

    points = []
    active = []

    place(rng.uniform(0, width), rng.uniform(0, height))

    while active:
        idx = rng.randrange(len(active))
        cx, cy = active[idx]

        placed_new = False
        for _ in range(k):
            angle = rng.uniform(0, math.tau)
            radius = rng.uniform(min_distance, 2 * min_distance)
            candidate_x = cx + math.cos(angle) * radius
            candidate_y = cy + math.sin(angle) * radius

            if fits(candidate_x, candidate_y):
                place(candidate_x, candidate_y)
                placed_new = True
                break

        if not placed_new:
            active.pop(idx)

    return points
