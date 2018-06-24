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

# Maximum distance from origin for cylinder
maxdist = 10

# Radius bounds for cylinder
minrad = 0.5
maxrad = 6

# Height bounds for cylinder
minheight = 0.5
maxheight = 6

# Create our camera
camera = Camera('location', [1.5*maxdist, 1.5*maxdist, 1.5*maxdist],
                'look_at', [0, 0, 0])

# Change to a folder to save the rendered image
current_dir = os.getcwd()
cylinder_dir = os.path.join(current_dir, "cylinder")
os.chdir(cylinder_dir)

# Number of cylinder images to generate
num_cylinders = 2000

for i in range(num_cylinders):

    # Determine radius
    radius = random.uniform(minrad, maxrad)
    
    # Determine cylinder height
    height = random.uniform(minheight, maxheight)
    
    # Generate location of cylinder center points
    bottom = [random.uniform(-1 * maxdist + radius, maxdist - radius),
              random.uniform(0, maxdist - height),
              random.uniform(-1 * maxdist + radius, maxdist - radius)]
    top = [bottom[0], bottom[1] + height, bottom[2]]
    
    # Generate random rgb value for cube
    color = [random.uniform(0,1), random.uniform(0,1), random.uniform(0,1)]
    
    # Create a cylinder
    cylinder = Cylinder(bottom, top, radius, Texture(Pigment('color', color)))
    
    # Add elements to our scene
    scene = Scene(camera, objects=[sun, sky, ground, cylinder],
                  included=["colors.inc"],
                  defaults=[Finish('ambient', 0.1, 'diffuse', 0.9)])
    
    # Render the image
    outfile = "{:04d}_cylinder_{:.1f}_{:.1f}_{:.1f}_r_{:.1f}_h_{:.1f}.png".format(
        i, bottom[0], bottom[1], bottom[2], radius, height)
    scene.render(outfile, width=800, height=600, antialiasing=0.01)





