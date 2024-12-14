from Vector3d import *
from Ray import *
import math

class Camera:
    def __init__(self, vFOV, aspect, lookFrom, lookAt, vUp):
        theta = math.radians(vFOV)
        half_height = math.tan(theta / 2)
        half_width = aspect * half_height

        self.origin = lookFrom
        self.w = (lookFrom - lookAt).normalized()
        self.u = (vUp.cross(self.w)).normalized()
        self.v = self.w.cross(self.u)

        self.lower_left_corner = self.origin - half_width * self.u - half_height * self.v - self.w
        self.horizontal = 2 * half_width * self.u
        self.vertical = 2 * half_height * self.v

    def getARay(self, s, t):
        direction = self.lower_left_corner + s * self.horizontal + t * self.vertical - self.origin
        return Ray(self.origin, direction)