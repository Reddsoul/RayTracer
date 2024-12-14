# Ray.py
class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction.normalized()

    def getOrigin(self):
        return self.origin

    def getDirection(self):
        return self.direction

    def getPointAtParameter(self, t):
        return self.origin + self.direction * t