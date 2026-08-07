from settings import FPS, DEFAULT_SIMULATION_SPEED


class SimulationClock:

    def __init__(self):
        self.simulation_fps = FPS
        self.speed = DEFAULT_SIMULATION_SPEED
        self.time = 0.0

    def update(self):
        dt = 1 / self.simulation_fps
        self.time += dt * self.speed

        return dt * self.speed
