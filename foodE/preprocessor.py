import os
import numpy as np
import tensorflow as tf



def scaling_mobilnet_v2(images, labels):
    '''
    This fonction will scale the input pixels between -1 and 1
    '''
    print('⭐️ Scaling_mobilnet_v2')
    return tf.keras.applications.mobilenet_v2.preprocess_input(tf.image.convert_image_dtype(images, tf.float32)), labels

def preprocessing(fonction, train, validation, test):
    '''
    This fonction will apply the 'fonction' to the train, validation and test sets.
    I.e. preprocessing(scaling_mobilnet_v2, train, validation, test)
    '''
    train = train.map(fonction, num_parallel_calls=tf.data.AUTOTUNE)
    validation = validation.map(fonction, num_parallel_calls=tf.data.AUTOTUNE)
    test = test.map(fonction, num_parallel_calls=tf.data.AUTOTUNE)

    print('⭐️ Preprocessing')
    
    AUTOTUNE = tf.data.AUTOTUNE
    train = train.cache().prefetch(buffer_size=AUTOTUNE)
    val = val.cache().prefetch(buffer_size=AUTOTUNE)
    test = test.cache().prefetch(buffer_size=AUTOTUNE)
    
    print('⭐️ Process_cache')

    return train, validation, test
