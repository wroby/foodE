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

    # Modify the environment variables and re-run the script for each subsequent model
    #test1 : data augmentation
    #test2 : dropout last layer
    #test3 : max pool
    #test4 : lr-e5
    #test5 : image size 224
    #test6 : l1
    #test7 : l2
    #test8 : l1l2


    l1 = [0,0,0,0,0,0.01,0,0.01]
    l2 = [0,0,0,0,0,0,0.01,0.01]
    lr = [0.0001,0.0001]
    augmentation = ["True","False","False","False","False","False","False","False"]
    pool= ["avg","avg","max","avg","avg","avg","avg","avg"]
    dropout=["False","True","False","False","False","False","False","False"]
    img_height = [96,96,96,96,224,96,96,96]
    img_width = [96,96,96,96,224,96,96,96]




    for trainable, l1, l2, lr, augmentation, pool, dropout, img_height, img_width, patience in\
            zip(trainable, l1, l2, lr, augmentation, pool, dropout, img_height, img_width, patience):

        os.environ['DATA_AUGMENTATION'] = str(augmentation)
        os.environ['DROPOUT'] = str(dropout)
        os.environ['POOL'] = str(pool)

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
        train,validation,test = get_local_data(img_height=img_height,img_width=img_width)
        print(f"\n✅ Local Data OK")
        train, validation, test = preprocessing(train,validation, test)
        print(f"\n✅ Data processed entirely")
        model = initialize_model(img_height=img_height,img_width=img_width,trainable=trainable,reg_l1=l1,reg_l2=l2)
        print(f"\n✅ initialized model")
        model = compiler(model,learning_rate=lr)
        print(f"\n✅ compiled model")
        model,history = fitting(model, train=train, validation = validation,patience=patience)

        #Get best val_accuracy
        best_val_acc = max(history.history["val_accuracy"])
        print(best_val_acc)
        best_epoch = history.history["val_accuracy"].index(best_val_acc)
        best_val_loss = history.history["val_loss"][best_epoch]
        best_loss = history.history["loss"][best_epoch]
        best_acc = history.history["accuracy"][best_epoch]

        #Evaluate
        test_accuracy = eval(model,test)

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
