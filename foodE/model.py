import os
import numpy as np
import time
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.efficientnet_v2 import EfficientNetV2B2
from tensorflow.keras import regularizers, layers, Sequential, Input, Model
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Convolution2D, MaxPooling2D, ZeroPadding2D, GlobalAveragePooling2D, AveragePooling2D
from tensorflow.keras.callbacks import EarlyStopping, TensorBoard
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import mixed_precision
import os
from foodE.custom_model import custom_model


def initialize_model(img_height:int=int(os.environ.get('IMG_HEIGHT')),\
                    img_width:int=int(os.environ.get('IMG_WIDTH')),trainable:bool=os.environ.get('TRAINABLE'),\
                    reg_l1 = float(os.environ.get('REGULARIZER_L1')), reg_l2 = float(os.environ.get('REGULARIZER_L2'))):

    """ Initialize CNN model"""
    model_choice = os.getenv("MODEL")

    #Setting the model based on the choice
    if model_choice == "MobileNetV2":
        base_model = MobileNetV2(include_top = False,
                                 input_shape = (img_height, img_width, 3),
                                 weights = "imagenet",
                                 pooling = "max")

    elif model_choice == "InceptionV3":
        base_model = InceptionV3(include_top=False,
                                 weights="imagenet",
                                 input_shape=(img_height, img_width, 3),
                                 pooling= "max")

    elif model_choice == "ResNet50":
        base_model = ResNet50(include_top = False,
                                 weights = "imagenet",
                                 pooling = "max",
                                 input_shape = (img_height, img_width, 3))


    elif model_choice == "VGG16":
        base_model = VGG16(include_top = False,
                           weights = "imagenet",
                           input_shape = (img_height, img_width, 3))

    elif model_choice == "EfficientNetB2":
        base_model = EfficientNetV2B2(include_top = False,
                                    weights = "imagenet",
                                    include_preprocessing = False,
                                    pooling="max",
                                    input_shape = (img_height, img_width, 3))

    elif model_choice == "Custom":
        #Define our own model
        base_model = custom_model(img_height, img_width)

    else:
        print("\u274c No model found, model must be : [MobilnetV2, InceptionV3,\
            ResNet50, VGG16, EfficientNetB2, Custom]")
        return None

    if trainable == "True":
        base_model.trainable = True
    else:
        base_model.trainable = False

    # Mixed Precision to speedup GPU
    #mixed_precision.set_global_policy('mixed_float16')

    regu = regularizers.L1L2(l1=reg_l1, l2=reg_l2)
    #Model Functionial
    inputs = Input(shape=(img_height,img_width,3))

    if os.getenv('DATA_AUGMENTATION') == 'True':
        x = layers.RandomFlip(mode="horizontal", seed=42)(inputs)
            # Apply rotation, height, and width randomizations
        x = layers.RandomRotation(factor=0.2, seed=42)(x)
            # Apply zoom randomization
        x = layers.RandomZoom(height_factor=(0.1,0.3),width_factor=(0.1,0.3), seed=42)(x)
    else:
        x = inputs
    x = base_model(x)

    x = layers.Dense(512, activation='relu')(x)
    x = layers.Dense(128, activation='relu')(x)
    #x = layers.GlobalAveragePooling2D()(x)
    if os.getenv('DROPOUT') == 'True':
        x = layers.Dropout(0.2)(x)
    outputs = layers.Dense(101,activation = "softmax",kernel_regularizer=regu)(x)

    model = Model(inputs = inputs, outputs= outputs)

    # Block training of BachNormalization
    for layer in model.layers:
        if isinstance(layer, layers.BatchNormalization):
            layer.trainable = False

    print(f"⭐️ Model built with Data augmentation : {os.environ.get('DATA_AUGMENTATION')}")
    print(f"⭐️ Model built with dropout : {os.environ.get('DROPOUT')}")
    print(f"⭐️ Model built with pool : {os.environ.get('POOL')}")
    print(f"⭐️ Model built with shape : {img_height} x {img_width}")
    print(f"⭐️ Model built with trainable : {trainable}")
    print(f"⭐️ Model built with l1 : {reg_l1}")
    print(f"⭐️ Model built with l2 : {reg_l2}")

    print(f"\u2705 Model {model_choice} initialize")
    print(model.get_config()['layers'][-1])

    ## Check policy for Mixed Precision
    for lnum, layer in enumerate(model.layers):
        print(lnum, layer.name, layer.trainable, layer.dtype, layer.dtype_policy)
    return model


def compiler(model,learning_rate:float=float(os.environ.get('LEARNING_RATE')),metrics:list=["accuracy"]):
    """Return a compiled model"""
    model.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss='categorical_crossentropy',
        metrics=metrics)

    print(f"⭐️ Model compiled with learning rate : {learning_rate}")
    print(model.optimizer.get_config())
    return model


def fitting(model=None,train=None,validation=None,patience:int=int(os.environ.get('PATIENCE'))\
            , epochs:int=int(os.environ.get('EPOCH')), batch_size:int=int(os.environ.get('BATCH_SIZE'))):

    #Early stopping
    es = EarlyStopping(monitor="val_loss",
                    patience=patience,
                    mode="auto",
                    restore_best_weights=True)

    print(f"⭐️ EarlyStopping with patience : {patience}")


    print(f"⭐️ Fitting with epochs : {epochs}")
    print(f"⭐️ Fitting with batch size : {batch_size}")

    #Start fit
    history = model.fit(
                train,
                epochs=epochs,
                verbose=1,
                validation_data=validation,
                shuffle=True,
                batch_size=batch_size,
                callbacks=[es])

    print(f"\u2705 Model fitting is DONE !")

    return model, history

def eval(model,test):
    results = model.evaluate(test, verbose=1)
    print(f"Test Accuracy: {results[1] * 100:.2f}%")
    return results[1]

def pred(model, img):
    #Checkez le type(img) pour le predict
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)),"raw_data/food-101/food-101-test/images")
    classes = [x for x in os.listdir(path) if os.path.isdir(os.path.join(path,x))]
    results = model.predict(img)
    idx = np.argmax(results)
    recipe = classes[idx]

    return recipe
