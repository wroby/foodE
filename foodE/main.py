import numpy as np
import pandas as pd
import os

from foodE.local_data import get_local_data
from foodE.preprocessor import preprocessing
from foodE.model import initialize_model, compiler, fitting, eval
from foodE.registery import save_model

# def get_data():
#     train, validation, test = get_local_data()
#     return train, validation, test

# def preprocess(train, validation, test):
#     return preprocessing(train,validation,test)

print(f"\n✅ Data processed entirely")


def training():
    train,validation,test = get_local_data()
    train, validation, test = preprocessing(train,validation, test)
    print(f"\n✅ Data processed entirely")
    model = initialize_model()
    print("initialized model")
    model = compiler(model)
    print("compiled model")
    model,history = fitting(model, train=train , validation = validation )

    #Get lowest val_accuracy
    val_acc = np.min(history.history['val_accuracy'])

    #Params to load to mlflow
    params = dict(
    # Model parameters
    learning_rate=os.getenv("LEARNING_RATE"),
    batch_size=os.getenv("BATCH_SIZE "),
    epochs = os.getenv("EPOCH"),
    regularizerl1 = os.getenv("REGULARIZER_L1"),
    regularizerl2 = os.getenv("REGULARIZER_L2"),
    patience=os.getenv("PATIENCE "),
    context="train")

    save_model(model = model, params = params, metrics = val_acc)

    # eval(model,test)
    # results = model.evaluate(test, verbose=1)
    # print(f"Test Accuracy: {results[1] * 100:.2f}%")
    return None















if __name__ == '__main__':
    # get_data()
    # preprocess()
    training()
    # # pred()
    # # evaluate()
