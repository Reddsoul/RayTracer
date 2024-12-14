import math
class Vector3d:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def distance(self, vec):
        diffx = self.x - vec.getX()
        diffy = self.y - vec.getY()
        diffz = self.z - vec.getZ()
        return math.sqrt(diffx**2 + diffy**2 + diffz**2)

    def dot(self, vec):
        return self.x * vec.getX() + self.y * vec.getY() + self.z * vec.getZ()

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getZ(self):
        return self.z

    def isZero(self):
        return self.x == 0 and self.y == 0 and self.z == 0

    def length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self):
        length = self.length()
        if length != 0:
            self.x /= length
            self.y /= length
            self.z /= length

    def normalized(self):
        length = self.length()
        if length != 0:
            return Vector3d(self.x / length, self.y / length, self.z / length)
        else:
            return Vector3d(0, 0, 0)

    def cross(self, vec):
        """Calculate the cross product of two vectors."""
        return Vector3d(
            self.y * vec.getZ() - self.z * vec.getY(),
            self.z * vec.getX() - self.x * vec.getZ(),
            self.x * vec.getY() - self.y * vec.getX()
        )

    def print(self, msg):
        print(f"{msg}: ({self.x}, {self.y}, {self.z})")

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def setZ(self, z):
        self.z = z

    def __add__(self, vec):
        return Vector3d(self.x + vec.getX(), self.y + vec.getY(), self.z + vec.getZ())

    def __iadd__(self, vec):
        self.x += vec.getX()
        self.y += vec.getY()
        self.z += vec.getZ()
        return self

    def __imul__(self, factor):
        self.x *= factor
        self.y *= factor
        self.z *= factor
        return self

    def __isub__(self, vec):
        self.x -= vec.getX()
        self.y -= vec.getY()
        self.z -= vec.getZ()
        return self

    def __itruediv__(self, den):
        self.x /= den
        self.y /= den
        self.z /= den
        return self

    def __mul__(self, factor):
        return Vector3d(self.x * factor, self.y * factor, self.z * factor)

    def __rmul__(self, factor):
        return self.__mul__(factor)

    def __sub__(self, vec):
        return Vector3d(self.x - vec.getX(), self.y - vec.getY(), self.z - vec.getZ())

    def __neg__(self):
        return Vector3d(-self.x, -self.y, -self.z)