import os
import numpy as np


def pred(model, img):
    #Checkez le type(img) pour le predict
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)),"raw_data/food-101/food-101-test/images")
    classes = sorted([x for x in os.listdir(path) if os.path.isdir(os.path.join(path,x))])
    results = model.predict(img)
    idx = np.argmax(results)
    recipe = classes[idx]

    return recipe
