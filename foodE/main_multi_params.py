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

def training():

    # Modify the environment variables and re-run the script for each subsequent model
    #test0 : trainable
    #test1 : l1
    #test2 : l2
    #test3 : l1l2
    #test4 : lr-e5
    #test5 : lr-e2
    #test6 : data-augmentation
    #test7 : max pool
    #test8 : No pool
    #test9 : dropout
    #test10 : imageSize-224
    #test11 : patience-20
    #test12 : AdamW?

    trainable = ["False","False","False","False","False","False","False","False","False","False","False", "False"]
    l1 = [0.0, 0.01, 0, 0.01, 0, 0, 0, 0, 0, 0, 0, 0]
    l2 = [0.0, 0, 0.01, 0.01, 0, 0, 0, 0, 0, 0, 0, 0]
    lr = [0.0001, 0.0001, 0.0001, 0.0001, 0.00001, 0.01, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001,0.0001]
    augmentation =["False","False","False","False","False","False","True","False","False","False","False", "False"]
    pool=["avg","avg","avg","avg","avg","avg","avg","max","None","avg","avg"]
    dropout=["False","False","False","False","False","False","False","False","False","True","False", "False"]
    img_height = ['96','96','96','96','96','96','96','96','96','96','224',"96"]
    img_width = ['96','96','96','96','96','96','96','96','96','96','224',"96"]
    patience = ['10','10','10','10','10','10','10','10','10','10','10',"20"]


    for trainable, l1, l2, lr, augmentation, pool, dropout, img_height, img_width, patience in zip(trainable, l1, l2, lr, augmentation, pool, dropout, img_height, img_width, patience):
        os.environ['TRAINABLE'] = str(trainable)
        os.environ['REGULARIZER_L1'] = str(l1)
        os.environ['REGULARIZER_L2'] = str(l2)
        os.environ['LEARNING_RATE'] = str(lr)
        os.environ['DATA_AUGMENTATION'] = str(augmentation)
        os.environ['DROPOUT'] = str(dropout)
        os.environ['POOL'] = str(pool)
        os.environ['IMG_HEIGHT'] = str(img_height)
        os.environ['IMG_WIDTH'] = str(img_width)
        os.environ['PATIENCE'] = str(patience)

        #Params
        print("⭐️ Params ⭐️")
        print(f"Trainable : {trainable}")
        print(f"L1 : {l1}")
        print(f"L2 : {l2}")
        print(f"lr : {lr}")
        print(f"Data Augmentation :{augmentation}")
        print(f"Dropout : {dropout}")
        print(f"Pooling : {pool}")
        print(f"Height : {img_height}")
        print(f"Width : {img_width}")
        print(f"Patience : {patience}")
        print("⭐️ Params ⭐️")

        #Run Model
        train,validation,test = get_local_data()
        print(f"\n✅ Local Data OK")
        train, validation, test = preprocessing(train,validation, test)
        print(f"\n✅ Data processed entirely")
        model = initialize_model()
        print(f"\n✅ initialized model")
        model = compiler(model)
        print(f"\n✅ compiled model")
        model,history = fitting(model, train=train, validation = validation)

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
        test_accuracy = test_acc
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
