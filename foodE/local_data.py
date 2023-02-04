import os
from tensorflow.keras.utils import image_dataset_from_directory




def get_local_data():
    path = os.environ.get("PATH_DATA")
    class_name = [x for x in os.listdir(path) if os.path.isdir(os.path.join(path,x))]
    img_height = int(os.environ.get("IMG_HEIGHT"))
    img_width = int(os.environ.get("IMG_WIDTH"))
    if os.getenv("CHECK") == "TRAIN":
        train = image_dataset_from_directory(path,label_mode="categorical", color_mode="rgb",
                                            class_names=class_name,
                                            labels='inferred',
                                            validation_split=0.2, subset="training",
                                            image_size=(img_height,img_width), interpolation="bilinear",
                                            crop_to_aspect_ratio=True,
                                            seed=42, shuffle=True, batch_size=32)

        validation = image_dataset_from_directory(path,label_mode="categorical", color_mode="rgb",
                                                class_names=class_name,
                                                labels='inferred',
                                                validation_split=0.2, subset="validation",
                                                image_size=(img_height,img_width), interpolation="bilinear",
                                                crop_to_aspect_ratio=True,
                                                seed=42, shuffle=True, batch_size=32)
        return train,validation,None

    elif os.getenv("CHECK") == "TEST":
        test = image_dataset_from_directory(path, label_mode="categorical", color_mode="rgb",
                                            class_names=class_name,
                                            image_size=(img_height,img_width),
                                            interpolation="bilinear",
                                            crop_to_aspect_ratio=True,
                                            seed=42, shuffle=True, batch_size=32)

        return None, None, test
