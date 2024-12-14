import random as R
from Vector3d import *
from Sphere import *
from Ray import *
from Constants import *
from Light import *
from Texture import *
from Particle import *

class Image:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = []

    def runRayTracer(self, camera, lights, spheres):
        for j in range(self.height - 1, -1, -1):
            for i in range(self.width):
                color = Vector3d(0, 0, 0)
                for _ in range(NUM_SUBRAYS):  # Antialiasing with sub-rays
                    u = (i + R.random()) / float(self.width)
                    v = (j + R.random()) / float(self.height)
                    ray = camera.getARay(u, v)
                    color += self.calculatePixelColor(ray, spheres, lights)
                color /= NUM_SUBRAYS
                self.pixels.append(Light.applyGammaCorrection(Texture.clampColor(color)))  # Clamp and apply gamma correction
        return self.pixels

    def calculatePixelColor(self, ray, spheres, lights, depth=0):
        if depth >= MAX_DEPTH:
            return Vector3d(0, 0, 0)

        hit_anything = False
        t_min = 0.001  # Avoid self-intersection
        closest_t = float('inf')
        closest_sphere = None

        # Find the closest sphere hit by the ray
        for sphere in spheres:
            hit, t = sphere.rayHitsSphere(ray)
            if hit and t_min < t < closest_t:
                hit_anything = True
                closest_t = t
                closest_sphere = sphere

        if hit_anything:
            # Compute intersection point and normal
            hit_point = ray.getPointAtParameter(closest_t)
            normal = (hit_point - closest_sphere.center).normalized()
            view_dir = -ray.getDirection()

            # Start with base color
            pixel_color = Vector3d(1, 1, 1)

            # Apply textures if specified
            if closest_sphere.reflection_type == "Stripe":
                pixel_color = Texture.generateStripeTexture(hit_point, Vector3d(.9, .2, .1), Vector3d(.1, .9, .2), A, B, VERTICAL)
            elif closest_sphere.reflection_type == "Checkerboard":
                pixel_color = Texture.generateCheckerboardTexture(hit_point, Vector3d(.01, .01, .01), Vector3d(0.9, 0.9, 0.9), A1, B1, A2, B2)
            elif closest_sphere.reflection_type == "Particle":
                # Set particle color and fade based on lifespan
                pixel_color = Vector3d(0.8, 0.8, 0.8)  # Light gray color
                if hasattr(closest_sphere, 'age') and hasattr(closest_sphere, 'lifespan'):
                    fade = 1.0 - closest_sphere.age / closest_sphere.lifespan
                    pixel_color *= fade

            # Handle "GLAZED" reflection
            if closest_sphere.reflection_type == "GLAZED":
                reflect_dir = (ray.getDirection() - 2 * ray.getDirection().dot(normal) * normal).normalized()
                reflect_ray = Ray(hit_point + reflect_dir * 0.001, reflect_dir)
                reflected_color = self.calculatePixelColor(reflect_ray, spheres, lights, depth + 1)

                reflection_strength = 0.5  # Adjust this as needed
                pixel_color = (1 - reflection_strength) * pixel_color + reflection_strength * reflected_color

            # Apply Blinn-Phong lighting
            for light in lights:
                shading = Light.calculateBlinnPhongShading(ray, hit_point, normal, light, view_dir)
                shadow_factor = Light.calculateShadows(ray, hit_point, normal, spheres, light, closest_sphere.shadow_type, SHADOW_FACTOR)
                pixel_color += Vector3d(shading, shading, shading) * shadow_factor

            # Clamp the color to avoid overflows
            pixel_color = Texture.clampColor(pixel_color)

            return pixel_color
        else:
            # Handle background color (gradient)
            unit_direction = ray.getDirection().normalized()
            t = 0.5 * (unit_direction.getY() + 1.0)
            start_color = Vector3d(1.0, 1.0, 1.0)
            end_color = Vector3d(0.1, 0.2, 1.0)
            return Texture.clampColor((1.0 - t) * start_color + t * end_color)
