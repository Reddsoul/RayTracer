import time
from Constants import *
from Image import *
from Vector3d import *
from Sphere import *
from Camera import *
from Particle import *
import math
import random as R

def bezier_curve(t, p0, p1, p2, p3):
    """Cubic Bézier curve: interpolates between p0, p1, p2, p3."""
    return (1 - t) ** 3 * p0 + \
           3 * (1 - t) ** 2 * t * p1 + \
           3 * (1 - t) * t ** 2 * p2 + \
           t ** 3 * p3

def compute_impact_times(e, y0, g):
    """Compute the times when the sphere impacts the ground."""
    impact_times = []
    y = y0
    v = 0
    t_current = 0

    while True:
        # Time until impact
        if v == 0:
            t_to_ground = math.sqrt(2 * y / -g)
        else:
            discriminant = v**2 + 2 * g * y
            if discriminant < 0:
                discriminant = 0  # Prevent negative discriminant
            t_to_ground = (-v - math.sqrt(discriminant)) / g

        t_next = t_current + t_to_ground

        # Record impact time
        impact_times.append(t_next)

        # Update position and velocity at impact
        v = -e * (v + g * t_to_ground)
        t_current = t_next

        if abs(v) < 0.1:
            # Sphere has effectively stopped bouncing
            break

    return impact_times

def animate_spheres(frame, total_frames, impact_times_sphere1, impact_times_sphere2):
    """Animate two spheres over time with smooth transitions and rolling away."""
    total_time = ANIMATION_DURATION  # Total animation time in seconds
    time_per_frame = total_time / total_frames
    t = frame * time_per_frame  # Current time in seconds

    g = -9.8  # Acceleration due to gravity (negative for downward)

    # Initial positions and parameters
    y0 = 5  # Initial height
    x1_start = -1  # Sphere 1 starts on the left
    x2_start = 1   # Sphere 2 starts on the right

    # Coefficients of restitution
    e1 = 0.3  # Sphere 1 (less bouncy)
    e2 = 0.8  # Sphere 2 (more bouncy)

    # Function to compute vertical position y(t)
    def compute_vertical_position(t, e):
        y = y0
        v = 0
        t_current = 0
        while t_current < t:
            # Time until impact
            if v == 0:
                t_to_ground = math.sqrt(2 * y / -g)
            else:
                discriminant = v**2 + 2 * g * y
                if discriminant < 0:
                    discriminant = 0  # Prevent negative discriminant
                t_to_ground = (-v - math.sqrt(discriminant)) / g

            t_next = t_current + t_to_ground
            if t < t_next:
                # Free fall or ascent
                dt = t - t_current
                y = y + v * dt + 0.5 * g * dt**2
                v = v + g * dt
                break
            else:
                # Update position and velocity at impact
                y = 0
                v = -e * (v + g * t_to_ground)
                t_current = t_next
                if abs(v) < 0.1:
                    # Sphere has effectively stopped bouncing
                    y = 0
                    break
        return max(y, 0)

    # Compute vertical positions
    y1 = compute_vertical_position(t, e1)
    y2 = compute_vertical_position(t, e2)

    # Function to compute when each sphere starts rolling
    def compute_t_roll_start(e):
        """Compute the total time until the sphere stops bouncing and starts rolling."""
        # Initial impact velocity when first hitting the ground
        v = -math.sqrt(2 * -g * y0)  # Negative because it's falling downwards
        t_current = 0

        while True:
            # After bounce, update velocity (upwards)
            v = -e * v  # Positive value since v was negative

            # Time to reach the peak height (v = 0)
            t_up = -v / g  # g is negative, so t_up is positive

            # Total time for this bounce (up and down)
            t_bounce = 2 * t_up

            # Accumulate time
            t_current += t_bounce

            # Velocity just before next impact (downwards)
            v = -v  # Negative value

            # Check if the bounce height is negligible
            if abs(v) < 0.1:
                # Sphere has effectively stopped bouncing
                break

        return t_current

    # Compute when each sphere stops bouncing and starts rolling
    t_roll_start1 = compute_t_roll_start(e1)
    t_roll_start2 = compute_t_roll_start(e2)

    # Function to compute horizontal position x(t) using Bézier curve
    def compute_horizontal_position(t, x_start, t_roll_start, direction):
        if t < t_roll_start:
            x = x_start
        else:
            # Define the duration of the rolling phase
            t_end = total_time  # or set a specific end time for rolling
            t_b = (t - t_roll_start) / (t_end - t_roll_start)
            t_b = max(0, min(t_b, 1))  # Clamp t_b between 0 and 1

            # Define control points for the Bézier curve
            p0 = x_start
            p1 = x_start + direction * 0.5  # Adjust control point as needed
            p2 = x_start + direction * 1.5  # Adjust control point as needed
            p3 = x_start + direction * 4    # Final position after rolling

            # Compute the horizontal position using the Bézier curve
            x = bezier_curve(t_b, p0, p1, p2, p3)
        return x

    # Compute horizontal positions
    x1 = compute_horizontal_position(t, x1_start, t_roll_start1, -1)
    x2 = compute_horizontal_position(t, x2_start, t_roll_start2, -2)

    # Update sphere positions
    pos_sphere1 = Vector3d(x1, y1, -2)
    pos_sphere2 = Vector3d(x2, y2, -2)

    return pos_sphere1, pos_sphere2


def main():
    aspect_ratio = WIDTH / HEIGHT
    start_time = time.time()

    # Lights
    light1 = Light(Vector3d(-2, 2, -1), AMBIENT, DIFFUSE, SPECULAR)
    light2 = Light(Vector3d(2, 2, -1), AMBIENT, DIFFUSE, SPECULAR)
    lights = [light1, light2]

    # Spheres
    sphere1 = Sphere(Vector3d(0, 0, -2), RADIUS, SHADOW_TYPE_SHARP, "GLAZED")
    sphere2 = Sphere(Vector3d(-1, 0, -1.5), RADIUS, SHADOW_TYPE_SMOOTH, "Stripe")
    groundSphere = Sphere(Vector3d(0, -100.5, -1), GROUND_RADIUS, SHADOW_TYPE_SHARP, "Checkerboard")
    spheres = [sphere1, sphere2, groundSphere]

    # Initial parameters
    total_frames = TOTAL_FRAMES
    total_time = ANIMATION_DURATION  # Total animation time in seconds
    time_per_frame = total_time / total_frames
    y0 = 5  # Initial height
    g = -9.8  # Acceleration due to gravity (negative for downward)
    e1 = 0.3  # Coefficient of restitution for sphere 1
    e2 = 0.8  # Coefficient of restitution for sphere 2
    delta_t = time_per_frame / 2  # Time threshold for detecting impacts

    # Precompute impact times for both spheres
    impact_times_sphere1 = compute_impact_times(e1, y0, g)
    impact_times_sphere2 = compute_impact_times(e2, y0, g)

    # Particle list
    particles = []


    # Precompute impact times for both spheres and assign indices
    impact_times_sphere1 = compute_impact_times(e1, y0, g)
    impact_times_sphere2 = compute_impact_times(e2, y0, g)
    impact_times_indices_sphere1 = list(enumerate(impact_times_sphere1))
    impact_times_indices_sphere2 = list(enumerate(impact_times_sphere2))

    # Initialize sets for processed impact indices
    processed_impacts_indices_sphere1 = set()
    processed_impacts_indices_sphere2 = set()

    for frame in range(total_frames):
        t = frame * time_per_frame

        # Animate camera
        look_from = Vector3d(3, 2.7, 6)
        look_at = Vector3d(0, 0, -1)
        # Create the camera for this frame

        v_up = Vector3d(0, 1, 0)
        camera = Camera(25, aspect_ratio, look_from, look_at, v_up)

        # Animate spheres
        pos_sphere1, pos_sphere2 = animate_spheres(frame, total_frames, impact_times_sphere1, impact_times_sphere2)
        sphere1.center = pos_sphere1
        sphere2.center = pos_sphere2

       # Update particles
        dt = time_per_frame
        particles = [p for p in particles if p.is_alive()]

        for particle in particles:
            particle.update(dt)

        # Check for impacts for sphere 1
        for idx, t_imp in impact_times_indices_sphere1:
            if pos_sphere1.getY() <= 0.1 and len(particles) < (MAX_PARTICLES / 2):
                # Generate particles for sphere 1
                for _ in range(N_PARTICLES):
                    if len(particles) >= (MAX_PARTICLES / 2) :
                        break  # Stop spawning if we reach MAX_PARTICLES
                    # Position on the ground around the impact point
                    offset = Vector3d(R.uniform(-0.2, 0.2), 0, R.uniform(-0.2, 0.2))
                    particle_pos = Vector3d(pos_sphere1.getX(), -.4, pos_sphere1.getZ()) + offset
                    # Velocity along the ground plane
                    velocity = Vector3d(R.uniform(-0.5, 0.5), 0, R.uniform(-0.5, 0.5))
                    lifespan = 0.5  # seconds
                    particle = Particle(particle_pos, 0.05, lifespan, velocity)
                    particles.append(particle)
                processed_impacts_indices_sphere1.add(idx)
                break  

        # Check for impacts for sphere 2
        for idx, t_imp in impact_times_indices_sphere2:
            if pos_sphere2.getY() <= 0.1 and len(particles) < (MAX_PARTICLES * 2):
                # Generate particles for sphere 2
                for _ in range(N_PARTICLES):
                    if len(particles) >= (MAX_PARTICLES * 2):
                        break  # Stop spawning if we reach MAX_PARTICLES
                    # Position on the ground around the impact point
                    offset = Vector3d(R.uniform(-0.2, 0.2), 0, R.uniform(-0.2, 0.2))
                    particle_pos = Vector3d(pos_sphere2.getX(), -.4, pos_sphere2.getZ()) + offset
                    # Velocity along the ground plane
                    velocity = Vector3d(R.uniform(-0.5, 0.5), 0, R.uniform(-0.5, 0.5))
                    lifespan = 0.5  # seconds
                    particle = Particle(particle_pos, 0.05, lifespan, velocity)
                    particles.append(particle)
                processed_impacts_indices_sphere2.add(idx)
                break  # No need to check other impacts in this frame

        # Combine spheres and particles for rendering
        spheres_to_render = spheres + particles

        # Render the frame
        image = Image(WIDTH, HEIGHT)
        pixels = image.runRayTracer(camera, lights=lights, spheres=spheres_to_render)

        # Save frame
        frame_number = f"{frame:03d}"
        filename = f"./output/frame_{WIDTH}x{HEIGHT}_{frame_number}.ppm"

        with open(filename, 'w') as file:
            file.write(f"P3\n{WIDTH} {HEIGHT}\n255\n")
            for pixel in pixels:
                ir = int(255.99 * pixel.getX())
                ig = int(255.99 * pixel.getY())
                ib = int(255.99 * pixel.getZ())
                file.write(f"{ir} {ig} {ib}\n")

        print(f"Frame {frame_number} rendered")

    end_time = time.time()
    total_seconds = int(end_time - start_time)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    print(f"Total render time: {hours:02d}:{minutes:02d}:{seconds:02d}")

if __name__ == '__main__':
    main()