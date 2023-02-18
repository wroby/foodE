from fastapi import FastAPI
from foodE.registery import model_load
from foodE.model import pred
import numpy as np
from typing import List
from pydantic import BaseModel
from starlette.responses import Response
from api.api import get_macronutrients
import time
from google.cloud import bigquery
import os
from google.oauth2 import service_account

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

    #link pred to food api

    nutri = get_macronutrients(predi)


    #big query
    file_path = os.path.abspath(__file__)
    parent_folder = os.path.dirname(os.path.dirname(file_path))
    key_path = os.path.join(parent_folder, "google_key.json")

    credentials = service_account.Credentials.from_service_account_file(key_path)

    client = bigquery.Client(credentials=credentials,project="foode-376420")
    dataset = "foodE"
    table = "macro"


    dataset_ref = client.dataset(dataset)
    table_ref = dataset_ref.table(table)


    user_id = 1
    date = time.strftime('%Y-%m-%d', time.gmtime(time.time()))
    calories = str(nutri['calories']["value"])
    fat = str(nutri['fat']["value"])
    carbs = str(nutri['carbs']["value"])
    protein = str(nutri['protein']["value"])
    portion = 1

    rows_to_insert =[
        {"UserID":user_id,"Date":date,"Prediction":str(predi),"Calories":float(calories),
         "Fat":float(fat),"Protein":float(protein),"Carbs":float(carbs),"Portion":portion
         }
    ]

    table = client.get_table(table_ref)
    result = client.insert_rows(table,rows_to_insert)

    if result == []:
        succes = 'Your data has been processed'

    # Return a plain text response containing the prediction & macronutrient results
    return Response(content=predi, media_type="text/plain"), Response(content=calories,media_type="text/plain"),\
            Response(content=carbs,media_type="text/plain"),Response(content=fat,media_type="text/plain"),\
                Response(content=protein,media_type="text/plain"),Response(content=succes, media_type="text/plain")
