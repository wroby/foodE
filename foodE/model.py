import os
import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.efficientnet_v2 import EfficientNetV2B2
from tensorflow.keras import regularizers, layers, Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Convolution2D, MaxPooling2D, ZeroPadding2D, GlobalAveragePooling2D, AveragePooling2D
from tensorflow.keras.callbacks import EarlyStopping, TensorBoard
from tensorflow.keras.optimizers import Adam
import os


def initialize_model(img_height:int=int(os.environ.get('IMG_HEIGHT')),\
                    img_width:int=int(os.environ.get('IMG_WIDTH')),trainable:bool=bool(os.environ.get('TRAINABLE')),\
                    reg_l1 = float(os.environ.get('REGULARIZER_L1')), reg_l2 = float(os.environ.get('REGULARIZER_L2'))):

    """ Initialize CNN model"""
    model_choice = os.getenv("MODEL")

    #Setting the model based on the choice
    if model_choice == "MobilnetV2":
        base_model = MobileNetV2(include_top = False,
                                 input_shape = (img_height, img_width, 3),
                                 weights = "imagenet",
                                 pooling = "avg")

    elif model_choice == "InceptionV3":
        base_model = InceptionV3(include_top=False,
                                 weights="imagenet",
                                 input_shape=(img_height, img_width, 3),
                                 pooling="avg")

    elif model_choice == "ResNet50":
        base_model = ResNet50(include_top = False,
                                 weights = "imagenet",
                                 pooling = "avg",
                                 input_shape = (img_height, img_width, 3))


    elif model_choice == "VGG16":
        base_model = VGG16(include_top = False,
                           weights = "imagenet",
                           input_shape = (img_height, img_width, 3))

    elif model_choice == "EfficientNetB2":
        base_model = EfficientNetV2B2(include_top = False,
                                    weights = "imagenet",
                                    include_preprocessing = False,
                                    input_shape = (img_height, img_width, 3))

    elif model_choice == "Custom":
        #Define our own model
        pass

    else:
        print("\u274c No model found, model must be : [MobilnetV2, InceptionV3,\
            ResNet50, VGG16, EfficientNetB2, Custom]")
        return None

    if model_choice != "Custom":
        base_model.trainable = trainable

    if os.getenv('DATA_AUGMENTATION') == 'True':
        augmentation_layer =Sequential([
        layers.RandomFlip(mode="horizontal", seed=42),
        layers.RandomRotation(factor=0.05, seed=42),
        layers.RandomContrast(factor=0.2, seed=42)])
        print(f"⭐️ Data augmentation layers : True")
    else:
        augmentation_layer = Sequential([
            layers.Layer()
        ])
        print(f"⭐️ Data augmentation layers : False")

    #Adding regularizer if condition met
    regu = regularizers.L1L2(l1=reg_l1, l2=reg_l2)

    # Adding Augmentation layer & Top layer
    model = Sequential([

    ## Data Augmentation layer
    augmentation_layer,

    ## Base model
    base_model,
    #Adding flatten layer needed for ResNetRs200
    layers.Flatten(),
    ## FNN
    layers.Dense(128,activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(101,kernel_regularizer=regu,activation='softmax')
    ])

    # Build model
    model.build(input_shape=(None, img_height, img_width, 3))
    print(f"⭐️ Model built with shape : {img_height} x {img_width}")
    print(f"⭐️ Model built with trainable : {trainable}")
    print(f"⭐️ Model built with l1 : {reg_l1}")
    print(f"⭐️ Model built with l2 : {reg_l2}")

    print(f"\u2705 Model {model_choice} initialize")
    return model


def compiler(model,learning_rate:float=float(os.environ.get('LEARNING_RATE')),metrics:list=["accuracy"]):
    """Return a compiled model"""
    model.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss='categorical_crossentropy',
        metrics=metrics)

    print(f"⭐️ Model compiled with learning rate : {learning_rate}")

    return model


def fitting(model=None,train=None,validation=None,patience:int=int(os.environ.get('PATIENCE')), epochs:int=int(os.environ.get('EPOCH')), batch_size:int=int(os.environ.get('BATCH_SIZE'))):

    #Early stopping
    es = EarlyStopping(monitor="val_loss",
                    patience=patience,
                    mode="auto",
                    restore_best_weights=True)

    print(f"⭐️ EarlyStopping with patience : {patience}")

    #Adding tensorboard to log the training and visiualize performance for each model?

    path_log = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if not os.path.exists(os.path.join(path_log,"tmp")):
        os.mkdir(os.path.join(path_log,"tmp"))
        os.mkdir(os.path.join(path_log,"tmp","logs"))
    tensorboard_callback = TensorBoard(log_dir=os.path.join(path_log,"tmp","logs"))

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
                callbacks=[es, tensorboard_callback])

    print(f"\u2705 Model fitting is DONE !")

    return model, history

def eval(model,test):
    results = model.evaluate(test, verbose=1)
    print(f"Test Accuracy: {results[1] * 100:.2f}%")

def predict(model, img):
    #Checkez le type(img) pour le predict
    path = "../raw_data/food-101/food-101-train/images"
    classes = [x for x in os.listdir(path) if os.path.isdir(os.path.join(path,x))]
    results = model.predict(img)
    idx = np.argmax(results)
    recipe = classes[idx]

    return recipe
