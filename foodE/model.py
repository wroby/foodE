from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2
from tensorflow.keras import regularizers, layers, Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Convolution2D, MaxPooling2D, ZeroPadding2D, GlobalAveragePooling2D, AveragePooling2D
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam



def initialize_model(img_height:int=256,img_width:int=256,trainable:bool=False,regularizer:bool=True):
    """ Initialize CNN model"""
    base_model = MobileNetV2(
    input_shape=(img_height, img_width, 3),
    include_top=False,
    weights='imagenet',
    pooling='avg')

    base_model.trainable = trainable

    #Adding regularizer if condition met
    if regularizer: regu=regularizers.l2(0.005)
    else: regu = None

    # Adding Augmentation layer & Top layer
    model = Sequential([
    ## Data Augmentation layer
    layers.RandomFlip(mode="horizontal", seed=42),
    layers.RandomRotation(factor=0.05, seed=42),
    layers.RandomContrast(factor=0.2, seed=42),
    ## Base model
    base_model,
    ## FNN
    layers.Dense(128,activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(101,kernel_regularizer=regu,activation='softmax')
    ])

    # Build model
    model.build(input_shape=(None, img_height, img_width, 3))

    return model


def compiler(model,learning_rate:float=1e-3,metrics:list=["accuracy"]):
    """Return a compiled model"""
    model.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss='categorical_crossentropy',
        metrics=metrics)

    return model


def fitting(model,train,validation,patience:int=3):
    #Early stopping
    es = EarlyStopping(monitor="val_loss",
                    patience=patience,
                    mode="min",
                    restore_best_weights=True)
    #Start fit
    history = model.fit(
                train,
                epochs=100,
                verbose=1,
                validation_data=validation,
                shuffle=True,
                batch_size=32,
                callbacks=[es])

    return model, history

def evaluate(model,test):
    results = model.evaluate(test, verbose=1)
    print(f"Test Accuracy: {results[1] * 100:.2f}%")
