import os
from tensorflow.keras.models import load_model

def model_load():
    #Need to add load model from mlflow

    # load model locally"
    file_path = os.path.abspath(__file__)
    Llocal_path = os.path.join(os.path.dirname(file_path),"models")
    model_path = os.path.join(Llocal_path, "EfficientNetB2-82")
    print(model_path)
    model = load_model(os.path.join(model_path,"efficientnet-82val-noda.h5"))
    #model = load_model(os.path.join(model_path,"model"))
    print("Loaded model from local Disk.")

    return model
