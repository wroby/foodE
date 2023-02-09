from tensorflow.keras import models
from tensorflow.keras import Sequential, layers
import os


#Architecture

def custom_model(img_height, img_width):

    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), input_shape=(img_height, img_width, 3), activation = 'relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Conv2D(32, (3, 3), activation = 'relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Flatten())
    model.add(layers.Dense(250,activation='relu'))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(101,activation='softmax'))

    return model
