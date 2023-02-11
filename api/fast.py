from fastapi import FastAPI
from foodE.registery import load_model
import numpy as np
from foodE.registery import save_model
import mlflow.keras
from tensorflow import keras

app = FastAPI()

app.state.model = model

@app.get("/predict")

def prediction(img):
    #Check input type
    model = app.state.model
    pred = model.predict(img)
    idx = np.argmax(pred)
    recipe = classes[idx]
    return recipe
