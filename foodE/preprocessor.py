import os
import numpy as np
import tensorflow as tf



def scaling_mobilnet_v2(images, labels):
    '''
    This fonction will scale the input pixels between -1 and 1
    '''
    preprocessing_data =  tf.keras.applications.mobilenet_v2.preprocess_input(tf.image.convert_image_dtype(images, tf.float32)), labels
    return preprocessing_data

def preprocessing(fonction, train, validation, test):
    '''
    This fonction will apply the 'fonction' to the train, validation and test sets.
    I.e. preprocessing(scaling_mobilnet_v2, train, validation, test)
    '''
    train = train.map(fonction, num_parallel_calls=tf.data.AUTOTUNE)
    validation = validation.map(fonction, num_parallel_calls=tf.data.AUTOTUNE)
    test = test.map(fonction, num_parallel_calls=tf.data.AUTOTUNE)
    return train, validation, test


def preprocess_cache(train, val, test):
    '''
    Cache the preprocessed data in memory and prefetch the next batch
    Cette fonction est-elle utilisée ?
    '''
    AUTOTUNE = tf.data.AUTOTUNE
    train = train.cache().prefetch(buffer_size=AUTOTUNE)
    val = val.cache().prefetch(buffer_size=AUTOTUNE)
    test = test.cache().prefetch(buffer_size=AUTOTUNE)

    return train, val, test
