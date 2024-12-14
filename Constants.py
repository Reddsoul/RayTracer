# Screen Size
WIDTH = 800
HEIGHT = 600

# Rays
NUM_SUBRAYS = 5

# Shadow Types
SHADOW_TYPE_SHARP = "Sharp"
SHADOW_TYPE_SMOOTH = "Smooth"

# Number of particles per impact
N_PARTICLES = 10
MAX_PARTICLES = 10

# Shadow Rays
NUM_SHADOWRAYS = 5

#Smooth Shadow Factor
#lower = sharper
#higher = softer
SHADOW_FACTOR = 1

SHADOW_MULT = 100

# Lighting
LIGHT_TYPE_BLINN_PHONG = "Blinn-Phong"

# Reflection
MAX_DEPTH = 50  # Maximum recursion depth for reflections

#Lights
# Darker scene: Lower ambient and diffuse.
# Sharper highlights: Increase specular.
# More balanced lighting: Increase diffuse slightly and reduce specular.
AMBIENT = 0.05
DIFFUSE = 0.05
SPECULAR = 0.1

#Gamma
GAMMA = .5

#Balls
RADIUS = 0.5

GROUND_RADIUS = 100

#Stripe
# A smaller number = thicker 
# A bigger number = thiner
# B positive = shift left
# B negative = shift right
A = 13
B = -1
VERTICAL = True

#Checker Board
A1=2.5
B1=0
A2=2.5
B2=0

# Animation
FRAMES_PER_SECOND = 24
ANIMATION_DURATION = 10  # Seconds
TOTAL_FRAMES = FRAMES_PER_SECOND * ANIMATION_DURATION