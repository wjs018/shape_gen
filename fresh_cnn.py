import os
import numpy as np

from time import time

from keras import models, layers, optimizers
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import TensorBoard

#Number of classes we are distinguishing between
n_classes = 4

#Build new CNN model
model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)))
model.add(layers.Conv2D(32, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D(pool_size=(2,2)))
model.add(layers.Dropout(0.25))

model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D(pool_size=(2,2)))
model.add(layers.Dropout(0.25))

model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D(pool_size=(2,2)))
model.add(layers.Dropout(0.25))

model.add(layers.Conv2D(256, (3, 3), activation='relu'))
model.add(layers.Conv2D(256, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D(pool_size=(2,2)))
model.add(layers.Dropout(0.25))

#Decision part of our model
model.add(layers.Flatten())
model.add(layers.Dense(1024, activation='relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(n_classes, activation='softmax'))

model.summary()

#Define directories
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
train_datagen = ImageDataGenerator(rescale=1./255,
                                   fill_mode='nearest')
test_datagen = ImageDataGenerator(rescale=1./255,
                                  fill_mode='nearest')
batch_size = 20

#Create the generators for importing images
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(224,224),
    batch_size=batch_size,
    class_mode='categorical')
test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(224,224),
    batch_size=batch_size,
    class_mode='categorical')

model.compile(optimizer=optimizers.RMSprop(lr=1e-4),
              loss='categorical_crossentropy',
              metrics=['acc'])
 
#Create the TensorBoard instance to call back to
tensorboard = TensorBoard(log_dir="logs/fresh/{}".format(time()),
                          write_graph=True,
                          write_images=True)

history = model.fit_generator(train_generator,
                              steps_per_epoch=train_generator.samples/train_generator.batch_size,
                              epochs=50,
                              validation_data=test_generator,
                              validation_steps=test_generator.samples/test_generator.batch_size,
                              callbacks=[tensorboard])

model.save('new_cnn.h5')