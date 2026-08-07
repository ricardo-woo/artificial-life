import random
import math


class OU_Noise:
    def __init__(self, mu=0.0, theta=0.15, sigma=0.2):
        self.mu = mu
        self.theta = theta
        self.sigma = sigma
        self.state = self.mu

    def step(self, dt):
        safe_dt = min(dt, 0.1)

        drift = self.theta * (self.mu - self.state) * safe_dt
        diffusion = self.sigma * math.sqrt(safe_dt) * random.gauss(0, 1)

        self.state += drift + diffusion
        return self.state
