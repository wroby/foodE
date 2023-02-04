import os
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.applications.resnet_rs import ResNetRS200
from tensorflow.keras import regularizers, layers, Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Convolution2D, MaxPooling2D, ZeroPadding2D, GlobalAveragePooling2D, AveragePooling2D
from tensorflow.keras.callbacks import EarlyStopping, TensorBoard
from tensorflow.keras.optimizers import Adam


def initialize_model(img_height:int=256,\
                    img_width:int=256,trainable:bool=True,regularizer:bool=False):
                    
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

    elif model_choice == "ResNetRs200":
        base_model = ResNetRS200(include_top = False,
                                 weights = "imagenet",
                                 include_preprocessing = False,
                                 input_shape = (img_height, img_width, 3))

    elif model_choice == "Local":
        #Define our own model
        pass

    else:
        print("\u274c No model found, model must be : [MobilnetV2, InceptionV3, ResNetRs200, Local]")
        return None

    if model_choice != "Local":
        base_model.trainable = trainable

    #Adding regularizer if condition met
    if regularizer: regu=regularizers.l2(0.005)
    else: regu = None

    # Adding Augmentation layer & Top layer
    model = Sequential([
    ## Data Augmentation layer

    # layers.RandomFlip(mode="horizontal", seed=42),
    # layers.RandomRotation(factor=0.05, seed=42),
    # layers.RandomContrast(factor=0.2, seed=42),

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

    print(f"\u2705 Model {model_choice} initialize")
    return model


def compiler(model,learning_rate:float=1e-3,metrics:list=["accuracy"]):
    """Return a compiled model"""
    model.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss='categorical_crossentropy',
        metrics=metrics)

    print(f"\u2705 Model compiled with learning rate : {learning_rate}")
    return model



def fitting(model=None,train=None,validation=None,patience:int=3):

    #Early stopping
    es = EarlyStopping(monitor="val_loss",
                    patience=patience,
                    mode="min",
                    restore_best_weights=True)

    #Adding tensorboard to log the training and visiualize performance for each model?


    path_log = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(path_log)
    if not os.path.exists(os.path.join(path_log,"tmp")):
        os.mkdir(os.path.join(path_log,"tmp"))
        os.mkdir(os.path.join(path_log,"tmp","logs"))
    tensorboard_callback = TensorBoard(log_dir=os.path.join(path_log,"tmp","logs"))

    #Start fit
    history = model.fit(
                train,
                epochs=100,
                verbose=1,
                validation_data=validation,
                shuffle=True,
                batch_size=32,
                callbacks=[es, tensorboard_callback])

    return model, history

def evaluate(model,test):
    results = model.evaluate(test, verbose=1)
    print(f"Test Accuracy: {results[1] * 100:.2f}%")
