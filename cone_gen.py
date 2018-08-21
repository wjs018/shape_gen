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

# Maximum distance from origin for cone
maxdist = 10

# Radius bounds for cone base
minedge = 0.5
maxedge = 6

# Height bounds for cone
minheight = 0.5
maxheight = 6

# Create our camera
camera = Camera('location', [1.5 * maxdist, 1.5 * maxdist, 1.5 * maxdist],
                'look_at', [0, 0, 0])

# Change to a folder to save the rendered image
data_dir = '/media/unraid/Datasets/shape_gen'

# Number of cone images to generate
num_cones = 2000

for i in range(num_cones):

    # Determine base radius
    base_radius = random.uniform(minedge, maxedge)
    
    # Determine cone height
    height = random.uniform(minheight, maxheight)
    
    # Generate location of cone center points
    bottom = [random.uniform(-1 * maxdist + base_radius, maxdist - base_radius),
              random.uniform(0, maxdist - height),
              random.uniform(-1 * maxdist + base_radius, maxdist - base_radius)]
    top = [bottom[0], bottom[1] + height, bottom[2]]
    
    # Generate random rgb value for cube
    color = [random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)]
    
    # Create a cone
    cone = Cone(bottom, base_radius, top, 0.0, Texture(Pigment('color', color)))
    
    # Add elements to our scene
    scene = Scene(camera, objects=[sun, sky, ground, cone],
                  included=["colors.inc"],
                  defaults=[Finish('ambient', 0.1, 'diffuse', 0.9)])
    
    # output filename
    outfile = "{:04d}_cone_{:.1f}_{:.1f}_{:.1f}_r_{:.1f}_h_{:.1f}.png".format(
        i, bottom[0], bottom[1], bottom[2], base_radius, height)
    
    # Render the image to the correct place, 20% of images for test set
    if i < 0.2 * num_cones:
        test_path = os.path.join(data_dir, 'test', 'cone')
        os.chdir(test_path)
        scene.render(outfile, width=244, height=244, antialiasing=0.01)
    else:
        train_path = os.path.join(data_dir, 'train', 'cone')
        os.chdir(train_path)
        scene.render(outfile, width=244, height=244, antialiasing=0.01)
