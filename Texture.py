import math
from Vector3d import *


class Texture:
    def clampColor(color):
        return Vector3d(
            min(1.0, max(0.0, color.getX())),
            min(1.0, max(0.0, color.getY())),
            min(1.0, max(0.0, color.getZ()))
        )

    def generateStripeTexture(hit_point, color1, color2, a, b, vertical):
        axis = hit_point.getZ() if vertical else hit_point.getX()
        return color1 if math.sin(a * axis + b) > 0 else color2

    def generateCheckerboardTexture(hit_point, color1, color2, a1, b1, a2, b2):
        x = hit_point.getX()
        z = hit_point.getZ()
        return color1 if (math.sin(a1 * x + b1) > 0) ^ (math.sin(a2 * z + b2) > 0) else color2