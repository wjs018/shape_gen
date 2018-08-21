import os
import numpy as np

from time import time

from keras import models, layers, optimizers
from keras.preprocessing.image import ImageDataGenerator
from keras.applications import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.callbacks import TensorBoard

#Number of classes we are distinguishing between
n_classes = 4

#Import a pre-trained CNN, but just the convolutional layers
vgg_conv = VGG16(weights='imagenet',
                 include_top=False,
                 input_shape=(224, 224, 3))

#Unfreeze the last four layers
for layer in vgg_conv.layers[:-4]:
    layer.trainable = False

for layer in vgg_conv.layers:
    print(layer, layer.trainable)

#Build new model by incorporating VGG model
new_model = models.Sequential()
new_model.add(vgg_conv)

#Add new dense layers, flattening input first
new_model.add(layers.Flatten())
new_model.add(layers.Dense(1024, activation='relu'))
new_model.add(layers.Dropout(0.5))
new_model.add(layers.Dense(n_classes, activation='softmax'))

new_model.summary()
 
train_dir = "/media/unraid/Datasets/shape_gen/train"
test_dir = "/media/unraid/Datasets/shape_gen/test"

#Count the number of .png files in the test and train data sets
n_train = 0
for root, dirs, files in os.walk(train_dir):
    for file in files:
        if file.endswith('.png'):
            n_train += 1

n_test = 0
for root, dirs, files in os.walk(test_dir):
    for file in files:
        if file.endswith(".png"):
            n_test += 1

#Generate our data using the preprocessing step from VGG16
datagen = ImageDataGenerator(preprocessing_function=preprocess_input,
                             fill_mode='nearest')
batch_size = 20

#Create the generators for importing images
train_generator = datagen.flow_from_directory(
    train_dir,
    target_size=(224,224),
    batch_size=batch_size,
    class_mode='categorical')
test_generator = datagen.flow_from_directory(
    test_dir,
    target_size=(224,224),
    batch_size=batch_size,
    class_mode='categorical')

new_model.compile(optimizer=optimizers.RMSprop(lr=1e-4),
              loss='categorical_crossentropy',
              metrics=['acc'])
 
#Create the TensorBoard instance to call back to
tensorboard = TensorBoard(log_dir="logs/vgg_fine/{}".format(time()),
                          write_graph=True,
                          write_images=True)

history = new_model.fit_generator(train_generator,
                                  steps_per_epoch=train_generator.samples/train_generator.batch_size,
                                  epochs=30,
                                  validation_data=test_generator,
                                  validation_steps=test_generator.samples/test_generator.batch_size,
                                  callbacks=[tensorboard])
 
new_model.save('fine_trained_model.h5')