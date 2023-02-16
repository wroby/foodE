from fastapi import FastAPI
from foodE.registery import model_load
from foodE.model import pred
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
import io
from PIL import Image

app = FastAPI()

app.state.model = model_load()

@app.post("/predict")

def receive_image(img): #: UploadFile=File(...)):

    ### Receiving and decoding the image
    #contents = await img.read()
    #contents = Image.open(contents)
    #contents = contents.resize((96,96))
    # nparr = np.fromstring(contents, np.uint8)
    #cv2_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR) # type(cv2_img) => numpy.ndarray
    #Check input type``
    #cv2_img = img.resize((96,96))
    #cv2_img

    model = app.state.model
    prediction = pred(model,img) #img = image tensor
    print(prediction)
