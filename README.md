# Shape Generation and Classification

This repository consists of code that generates basic three dimensional shapes and renders images of them. It also includes different image classification scripts using Convolutional Neural Networks to classify the images by shape.

Images are generated through POV-Ray using the [Vapory](https://github.com/Zulko/vapory) library. Image classification is done through Tensorflow using Keras.

## Image generation

Images are of isolated shapes belonging to one of four classes: cone, cube, cylinder, and sphere. The location, size, and color are all randomly generated within the scene. Dimensions of the shapes are randomized as well (within reason) so that not every shape of the same type is self-similar. For example, there are short and wide cylinders as well as tall and narrow cylinders. At the moment, orientation of the shapes are kept the same across all images. The other elements of the scene (camera location, light source, ground) are kept consistent for every image.

In the generation scripts, `<shape>_gen.py`, ther `data_dir` variable defines where the images are saved. That folder should be the same for all the shape generation files as subfolders are programatically defined. 20% of the images will be put into a `test` folder. These images are not used for training and are the validation set for our model.

## Image Classification

There are three models implemented so far. The first is found in `fresh_cnn.py`. This defines a new, untrained CNN roughly following a similar template to the VGG model. This model achieves a test set accuracy of 0.975 after ~40 epochs.

The second model, `vgg_classifier.py`, uses pre-trained weights from the VGG16 model, using transfer learning to boost training time. This model only trains the dense decision layers after the convolutional layers. It matches the performance of `fresh_cnn.py` with a test set accuracy of 0.9765 after only 20 epochs.

The third model, `vgg_classifier_fine.py` also uses the pre-trained weights of the VGG16 model, but allows for the final four convolutional layers to be trained alongside the dense decision making layers. This fine tuning allows for an improved 0.99 accuracy on the test set after 30 epochs.

## Requirements

I have built and run this in Python 3.6.6. I am unsure if this would work for Python 2.7+, but don't *a priori* see where a problem would arise.

These libraries are required to run the code in this repository:

* `vapory` is used to render objects using POV-Ray ([Github](https://github.com/Zulko/vapory))
    - version used: 0.1.01
* `tensorflow` is used as the backend for Keras
    - version used: 1.10.0 using CUDA 9.0, CUDNN 7.0.5, on a 1080 Ti
* `tensorboard` is used to monitor training progress and compare model results
    - version used: 1.10.0
* `keras` is used to build and train the models using tensorflow
    - version used: 2.2.2

## Contact

Feel free to reach out with questions/issues or make pull requests with optimizations and compatibility fixes. I can be reached at wjs018@gmail.com
