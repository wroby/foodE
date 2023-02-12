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
    model,history = fitting(model, train=test , validation = validation)

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

    # #Confusion matrix
    # true_label = []
    # predict_label = []

    # for images,labels in test:
    #     true_label.extend(np.argmax(labels,axis=1).tolist())
    #     predict = model.predict(images)
    #     predict_label.extend(np.argmax(predict,axis=1).tolist())
    # true_label = np.array(true_label)
    # predict_label = np.array(predict_label)

    # cm = confusion_matrix(true_label, predict_label)

    # #Classification report
    # report = classification_report(true_label,predict_label,\
    #     target_names=['apple_pie', 'baby_back_ribs', 'baklava', 'beef_carpaccio', 'beef_tartare', 'beet_salad', 'beignets', 'bibimbap', 'bread_pudding', 'breakfast_burrito', 'bruschetta', 'caesar_salad', 'cannoli', 'caprese_salad', 'carrot_cake', 'ceviche', 'cheese_plate', 'cheesecake', 'chicken_curry', 'chicken_quesadilla', 'chicken_wings', 'chocolate_cake', 'chocolate_mousse', 'churros', 'clam_chowder', 'club_sandwich', 'crab_cakes', 'creme_brulee', 'croque_madame', 'cup_cakes', 'deviled_eggs', 'donuts', 'dumplings', 'edamame', 'eggs_benedict', 'escargots', 'falafel', 'filet_mignon', 'fish_and_chips', 'foie_gras', 'french_fries', 'french_onion_soup', 'french_toast', 'fried_calamari', 'fried_rice', 'frozen_yogurt', 'garlic_bread', 'gnocchi', 'greek_salad', 'grilled_cheese_sandwich', 'grilled_salmon', 'guacamole', 'gyoza', 'hamburger', 'hot_and_sour_soup', 'hot_dog', 'huevos_rancheros', 'hummus', 'ice_cream', 'lasagna', 'lobster_bisque', 'lobster_roll_sandwich', 'macaroni_and_cheese', 'macarons', 'miso_soup', 'mussels', 'nachos', 'omelette', 'onion_rings', 'oysters', 'pad_thai', 'paella', 'pancakes', 'panna_cotta', 'peking_duck', 'pho', 'pizza', 'pork_chop', 'poutine', 'prime_rib', 'pulled_pork_sandwich', 'ramen', 'ravioli', 'red_velvet_cake', 'risotto', 'samosa', 'sashimi', 'scallops', 'seaweed_salad', 'shrimp_and_grits', 'spaghetti_bolognese', 'spaghetti_carbonara', 'spring_rolls', 'steak', 'strawberry_shortcake', 'sushi', 'tacos', 'takoyaki', 'tiramisu', 'tuna_tartare', 'waffles'])

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
