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
minedge = 0.5
maxedge = 6

# Create our camera
camera = Camera('location', [1.5*maxdist, 1.5*maxdist, 1.5*maxdist],
                'look_at', [0, 0, 0])

# Change to a folder to save the rendered image
current_dir = os.getcwd()
cube_dir = os.path.join(current_dir, "cube")
os.chdir(cube_dir)

# Number of sphere images to generate
num_cubes = 2000

for i in range(num_cubes):

    # Determine edge length
    edge = random.uniform(minedge, maxedge)
    
    # Generate location of cube corners
    bottom = [random.uniform(-1 * maxdist, maxdist - edge),
              random.uniform(0, maxdist - edge),
              random.uniform(-1 * maxdist, maxdist - edge)]
    top = [bottom[0] + edge, bottom[1] + edge, bottom[2] + edge]
    
    # Generate random rgb value for cube
    color = [random.uniform(0,1), random.uniform(0,1), random.uniform(0,1)]
    
    # Create a cube
    cube = Box(bottom, top, Texture(Pigment('color', color)))
    
    # Add elements to our scene
    scene = Scene(camera, objects=[sun, sky, ground, cube],
                  included=["colors.inc"],
                  defaults=[Finish('ambient', 0.1, 'diffuse', 0.9)])
    
    # Render the image
    outfile = "{:04d}_cube_{:.1f}_{:.1f}_{:.1f}_r_{:.1f}".format(
        i, bottom[0], bottom[1], bottom[2], edge)
    scene.render(outfile, width=800, height=600, antialiasing=0.01)





