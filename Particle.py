from Constants import *
from Sphere import *

class Particle(Sphere):
    def __init__(self, center, radius, lifespan, velocity):
        super().__init__(center, radius, SHADOW_TYPE_SHARP, "Particle")
        self.lifespan = lifespan
        self.age = 0
        self.velocity = velocity

    def update(self, dt):
        self.age += dt
        # Update position
        self.center += self.velocity * dt

    def is_alive(self):
        return self.age < self.lifespan