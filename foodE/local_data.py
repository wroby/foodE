import os
from tensorflow.keras.utils import image_dataset_from_directory

img_height = os.environ.get("img_height")
img_width = os.environ.get("img_width")


def get_local_data(path, path_test):
    train = image_dataset_from_directory(path,label_mode="categorical", color_mode="rgb",
                                         labels='inferred',
                                         validation_split=0.2, subset="training",
                                         image_size=(img_height,img_width), interpolation="bilinear",
                                         crop_to_aspect_ratio=True,
                                         seed=42, shuffle=True, batch_size=32)

    validation = image_dataset_from_directory(path,label_mode="categorical", color_mode="rgb",
                                              labels='inferred',
                                              validation_split=0.2, subset="validation",
                                              image_size=(img_height,img_width), interpolation="bilinear",
                                              crop_to_aspect_ratio=True,
                                              seed=42, shuffle=True, batch_size=32)

    test = image_dataset_from_directory(path_test, label_mode="categorical", color_mode="rgb",
                                        image_size=(img_height,img_width),
                                        interpolation="bilinear",
                                        crop_to_aspect_ratio=True,
                                        seed=42, shuffle=True, batch_size=32)

    return train, validation, test




t
