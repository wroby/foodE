from fastapi import FastAPI
from foodE.registery import load_model
import numpy as np
from foodE.registery import save_model

app = FastAPI()

app.state.model = load_model()

@app.get("/predict")

# def prediction(img):
#     model = app.state.model
#     pred = model.predict(img)
#     idx = np.argmax(pred)
#     recipe = classes[idx]
#     return recipe
