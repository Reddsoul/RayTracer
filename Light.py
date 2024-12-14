from Vector3d import *
from Constants import *
from Ray import *
import random as R


class Light:
    def __init__(self, position, ambient, diffuse, specular):
        self.position = position
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular

    def getPosition(self):
        return self.position

    def calculateBlinnPhongShading(ray, hit_point, normal, light, view_dir):
        light_dir = (light.getPosition() - hit_point).normalized()
        ambient = light.ambient

        # Diffuse shading
        diff = max(normal.dot(light_dir), 0.0)
        diffuse = light.diffuse * diff

        # Specular shading
        reflect_dir = (2 * normal.dot(light_dir) * normal - light_dir).normalized()
        spec = pow(max(view_dir.dot(reflect_dir), 0.0), 16)  # Shininess factor
        specular = light.specular * spec

        return ambient + diffuse + specular

    def calculateShadows(ray, hit_point, normal, spheres, light, shadow_type, smoothness_factor):
        shadow_hits = 0
        total_rays = 1 if shadow_type == SHADOW_TYPE_SHARP else NUM_SHADOWRAYS

        for _ in range(total_rays):
            if shadow_type == SHADOW_TYPE_SMOOTH:
                # Adjust the offset size based on the smoothness factor
                random_offset = Vector3d(
                    R.uniform(-smoothness_factor, smoothness_factor),
                    R.uniform(-smoothness_factor, smoothness_factor),
                    R.uniform(-smoothness_factor, smoothness_factor)
                )
                perturbed_light = light.getPosition() + random_offset
                shadow_dir = (perturbed_light - hit_point).normalized()
            
            else:
                shadow_dir = (light.getPosition() - hit_point).normalized()

            shadow_ray = Ray(hit_point + shadow_dir * 0.001, shadow_dir)  # Offset to prevent self-shadowing

            for sphere in spheres:
                hit, _ = sphere.rayHitsSphere(shadow_ray)
                if hit:
                    shadow_hits += 1
                    break  # Exit the loop early if any object is hit

        shadow_ratio = shadow_hits / total_rays
        shadow_percentage = (1 - shadow_ratio) ** SHADOW_MULT 
        return shadow_percentage  # Reduce light based on shadow percentage

    def applyGammaCorrection(color, gamma=GAMMA):
        inv_gamma = 1.0 / gamma
        return Vector3d(
            pow(color.getX(), inv_gamma),
            pow(color.getY(), inv_gamma),
            pow(color.getZ(), inv_gamma)
        )