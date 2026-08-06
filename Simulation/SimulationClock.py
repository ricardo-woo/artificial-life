from settings import FPS


class SimulationClock:

    def __init__(self):
        self.simulation_fps = FPS
        self.speed = 20
        self.time = 0.0

    def update(self):
        dt = 1 / self.simulation_fps
        self.time += dt * self.speed

        return dt * self.speed
