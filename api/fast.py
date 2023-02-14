from fastapi import FastAPI
from foodE.registery import model_load
import numpy as np
import mlflow.keras
from tensorflow import keras

app = FastAPI()

#app.state.model = "/Users/roubylouis/code/wroby/foodE/foodE/models/Custom_1676401626.8029408/model"

app.state.model = model_load


@app.get("/predict")

def prediction(img):
    #Check input type
    model = app.state.model
    pred = model.predict(img) #img = image tensor
    idx = np.argmax(pred)
    recipe = classes[idx]
    return recipe
