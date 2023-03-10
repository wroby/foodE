import os
import numpy as np
import tensorflow as tf



def scaling_model(images, labels):
    '''
    This fonction will scale the input pixels between -1 and 1
    '''
    print('⭐️ Scaling')
    if os.getenv("MODEL") == "MobileNetV2":
        return tf.keras.applications.mobilenet_v2.preprocess_input(tf.image.convert_image_dtype(images, tf.float32)), labels
    elif os.getenv("MODEL") == "InceptionV3":
        return tf.keras.applications.inception_v3.preprocess_input(tf.image.convert_image_dtype(images, tf.float32)), labels
    elif os.getenv("MODEL") == "ResNet50":
        return tf.keras.applications.resnet_rs.preprocess_input(tf.image.convert_image_dtype(images, tf.float32)), labels
    elif os.getenv("MODEL") == "VGG16":
        return tf.keras.applications.vgg16.preprocess_input(tf.image.convert_image_dtype(images, tf.float32)), labels
    elif os.getenv("MODEL") == "EfficientnetB2":
        return tf.keras.applications.efficientnet.preprocess_input(tf.image.convert_image_dtype(images, tf.float32)), labels
    else:
        return tf.keras.applications.mobilenet_v2.preprocess_input(tf.image.convert_image_dtype(images, tf.float32)), labels


def preprocessing(train, validation, test):
    '''
    This fonction will apply the 'fonction' to the train, validation and test sets.
    I.e. preprocessing(scaling_mobilnet_v2, train, validation, test)
    '''
    train = train.map(scaling_model, num_parallel_calls=tf.data.AUTOTUNE)
    validation = validation.map(scaling_model, num_parallel_calls=tf.data.AUTOTUNE)
    test = test.map(scaling_model, num_parallel_calls=tf.data.AUTOTUNE)

    print('⭐️ Preprocessing')

    AUTOTUNE = tf.data.AUTOTUNE
    train = train.cache().prefetch(buffer_size=AUTOTUNE)
    validation = validation.cache().prefetch(buffer_size=AUTOTUNE)
    test = test.cache().prefetch(buffer_size=AUTOTUNE)

    print('⭐️ Process_cache')

    return train, validation, test
