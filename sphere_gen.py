import os
import random

from vapory import *

random.seed(1)

sun = LightSource([1000, 2500, -2500], 'color', 'White')

sky = SkySphere(Pigment('gradient', [0, 1, 0],
                         ColorMap([0.0, 'color', 'White'],
                                  [0.5, 'color', 'CadetBlue'],
                                  [1.0, 'color', 'CadetBlue']),
                         "quick_color", "White"))

ground = Plane([0, 1, 0], 0,
                Texture(Pigment('color', [0.85, 0.55, 0.30]),
                         Finish('phong', 0.1)
                      )
                )

# Maximum distance from origin for center of sphere
maxdist = 10

# Radius bounds for sphere
minrad = 0.5
maxrad = 6

# Create our camera
camera = Camera('location', [1.5*maxdist, 1.5*maxdist, 1.5*maxdist],
                'look_at', [0, 0, 0])

# Change to a folder to save the rendered image
current_dir = os.getcwd()
sphere_dir = os.path.join(current_dir, "sphere")
os.chdir(sphere_dir)

# Number of sphere images to generate
num_spheres = 2000

for i in range(num_spheres):

    # Determine radius
    radius = random.uniform(minrad, maxrad)
    
    # Generate location of sphere center
    center = [random.uniform(-1 * maxdist + radius, maxdist - radius),
              random.uniform(0 + radius, maxdist - radius),
              random.uniform(-1 * maxdist + radius, maxdist - radius)]
    
    # Generate random rgb value for sphere
    color = [random.uniform(0,1), random.uniform(0,1), random.uniform(0,1)]
    
    # Create a sphere
    sphere = Sphere(center, radius, Texture(Pigment('color', color)))
    
    # Add elements to our scene
    scene = Scene(camera, objects=[sun, sky, ground, sphere],
                  included=["colors.inc"],
                  defaults=[Finish('ambient', 0.1, 'diffuse', 0.9)])
    
    # Render the image
    outfile = "{:04d}_sphere_{:.1f}_{:.1f}_{:.1f}_r_{:.1f}".format(
        i, center[0], center[1], center[2], radius)
    scene.render(outfile, width=800, height=600, antialiasing=0.01)





