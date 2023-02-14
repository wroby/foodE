import numpy as np
import pandas as pd
import os

from foodE.local_data import get_local_data
from foodE.preprocessor import preprocessing
from foodE.model import initialize_model, compiler, fitting, eval
from foodE.registery import save_model, save_classification_report, save_confusion_matrix, save_plot

# def get_data():
#     train, validation, test = get_local_data()
#     return train, validation, test

# def preprocess(train, validation, test):
#     return preprocessing(train,validation,test)

def training():
    train,validation,test = get_local_data()
    print(f"\n✅ Local Data OK")
    train, validation, test = preprocessing(train,validation, test)
    print(f"\n✅ Data processed entirely")
    model = initialize_model()
    print(f"\n✅ initialized model")
    model = compiler(model)
    print(f"\n✅ compiled model")
    model,history = fitting(model, train=train , validation = validation)

    #Get best val_accuracy
    best_val_acc = max(history.history["val_accuracy"])
    print(best_val_acc)
    best_epoch = history.history["val_accuracy"].index(best_val_acc)
    best_val_loss = history.history["val_loss"][best_epoch]
    best_loss = history.history["loss"][best_epoch]
    best_acc = history.history["accuracy"][best_epoch]

    #Evaluate
    eval(model,test)
    results = model.evaluate(test, verbose=1)
    test_accuracy = results[1]
    print(f"Test Accuracy: {results[1] * 100:.2f}%")

    metrics = dict(
    val_acc = best_val_acc,
    val_loss = best_val_loss,
    acc = best_acc,
    loss = best_loss,
    epoch = best_epoch,
    test_acc = test_accuracy
    )

    #Params to load to mlflow
    params = dict(
    # Model parameters
    learning_rate=os.getenv("LEARNING_RATE"),
    batch_size=os.getenv("BATCH_SIZE"),
    epochs = os.getenv("EPOCH"),
    regularizerl1 = os.getenv("REGULARIZER_L1"),
    regularizerl2 = os.getenv("REGULARIZER_L2"),
    patience=os.getenv("PATIENCE "),
    trainanble=os.getenv("TRAINABLE"),
    context="train")

    save_model(model = model, params = params, metrics = metrics)
    save_plot(history)
    save_confusion_matrix(model,test)
    save_classification_report()



    return None















if __name__ == '__main__':
    # get_data()
    # preprocess()
    training()
    # # pred()
    # # evaluate()
