from fastapi import FastAPI
from foodE.registery import model_load
from foodE.model import pred
import numpy as np
from typing import List
from pydantic import BaseModel
from starlette.responses import Response

# Create a new instance of the FastAPI application
app = FastAPI()

# Load the machine learning model and save it in the state of the application
app.state.model = model_load()

# Define a data model for the request body
class Img(BaseModel):
    img: List

# Define an HTTP endpoint that expects an HTTP POST request
# with a JSON payload containing a list of images
@app.post("/predict/")
async def receive_image(img: Img):
    # Get the list of images from the request body
    img_list = list(img)[0][1]

    # Convert the list of images to a numpy array
    img_array = np.array(img_list)

    # Add an extra dimension to the numpy array to create a tensor
    img_expand = np.expand_dims(img_array, axis=0)

    # Get the machine learning model from the application state
    model = app.state.model

    # Make a prediction using the machine learning model and the image tensor
    predi = pred(model, img_expand) #img = image tensor

    # Return a plain text response containing the prediction
    return Response(content=predi, media_type="text/plain")
