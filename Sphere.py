import math
from Vector3d import *

class Sphere:
    def __init__(self, center, radius, shadow_type='Sharp', reflection_type='None', fuzziness=0):
        self.center = center
        self.radius = radius
        self.shadow_type = shadow_type
        self.reflection_type = reflection_type
        self.fuzziness = fuzziness

    def rayHitsSphere(self, ray):
        oc = ray.getOrigin() - self.center
        a = ray.getDirection().dot(ray.getDirection())
        b = 2.0 * oc.dot(ray.getDirection())
        c = oc.dot(oc) - self.radius * self.radius
        discriminant = b * b - 4 * a * c

        if discriminant < 0:
            return False, None
        else:
            sqrt_disc = math.sqrt(discriminant)
            t1 = (-b - sqrt_disc) / (2.0 * a)
            t2 = (-b + sqrt_disc) / (2.0 * a)
            t = min(t1, t2)
            if t < 0:
                t = max(t1, t2)
                if t < 0:
                    return False, None
            return True, t
        
