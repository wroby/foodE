import numpy as np
import pandas as pd
import os

from foodE.local_data import get_local_data
from foodE.preprocessor import preprocessing
from foodE.model import initialize_model, compiler, fitting, eval

def get_data():
    train, validation, test = get_local_data
    return train, validation, test

# def preprocess(train, validation, test):
#     return preprocessing(train,validation,test)

print(f"\n✅ Data processed entirely")


def training():
    train, validation, test = preprocessing(train,validation, test)
    print(f"\n✅ Data processed entirely")
    model = initialize_model()
    print("initialized model")
    model = compiler(model)
    print("compiled model")
    model,history = fitting(model, train=train , validation = validation )
    eval(model,test)
    results = model.evaluate(test, verbose=1)
    print(f"Test Accuracy: {results[1] * 100:.2f}%")
    return None















if __name__ == '__main__':
    # get_data()
    # preprocess()
    training()
    # # pred()
    # # evaluate()
