import os
import numpy as np

from time import time

from keras import models, layers, optimizers
from keras.preprocessing.image import ImageDataGenerator
from keras.applications import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.callbacks import TensorBoard

#Import a pre-trained CNN, but just the convolutional layers
vgg_conv = VGG16(weights='imagenet',
                 include_top=False,
                 input_shape=(224, 224, 3))

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

#Last layer has dimensions of 7 x 7 x 512
#print(vgg_conv.summary())
n_classes = 4

#Generate our data using the preprocessing step from VGG16
datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
batch_size = 20

#Define the input and output of our convolutional layers
train_features = np.zeros(shape=(n_train, 7, 7, 512))
train_labels = np.zeros(shape=(n_train, n_classes))
test_features = np.zeros(shape=(n_test, 7, 7, 512))
test_labels = np.zeros(shape=(n_test, n_classes))

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

#Train our convolutional layers on the train images
i = 0
for inputs_batch, labels_batch in train_generator:
    #Run our first batch of images through the CNN layers
    features_batch = vgg_conv.predict(inputs_batch)
    train_features[i * batch_size : (i + 1) * batch_size] = features_batch
    train_labels[i * batch_size : (i + 1) * batch_size] = labels_batch
    i += 1
    # If we have finished all the batches, end the loop
    if i * batch_size >= n_train:
        break

train_features = np.reshape(train_features, (n_train, 7 * 7 * 512))

#Get the features for the test set as well
i = 0
for inputs_batch, labels_batch in test_generator:
    #Run our first batch of images through the CNN layers
    features_batch = vgg_conv.predict(inputs_batch)
    test_features[i * batch_size : (i + 1) * batch_size] = features_batch
    test_labels[i * batch_size : (i + 1) * batch_size] = labels_batch
    i += 1
    # If we have finished all the batches, end the loop
    if i * batch_size >= n_test:
        break

test_features = np.reshape(test_features, (n_test, 7 * 7 * 512))

#Save the features data
np.save('train_features', train_features)
np.save('test_features', test_features)

#Create the dense layers that will be the classification model
model = models.Sequential()
model.add(layers.Dense(1024, activation='relu', input_dim= 7 * 7 * 512))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(n_classes, activation='softmax'))

model.compile(optimizer=optimizers.RMSprop(lr=2e-4),
              loss='categorical_crossentropy',
              metrics=['acc'])

#Create the TensorBoard instance to call back to
tensorboard = TensorBoard(log_dir="logs/vgg/{}".format(time()),
                          write_graph=True,
                          write_images=True)

history = model.fit(train_features,
                    train_labels,
                    epochs=20,
                    batch_size=batch_size,
                    validation_data=(test_features, test_labels),
                    callbacks=[tensorboard])

model.save('trained_model.h5')