import mlflow
import time
from mlflow.tracking import MlflowClient
import os

import mlflow.keras
from tensorflow import keras



def save_model(model: keras.Model = None,
               params: dict = None,
               metrics: dict = None) -> None:
    """
    persist trained model, params and metrics
    """

    if os.getenv("MODEL_TARGET") == "mlflow":

        # retrieve mlflow env params
        track = os.getenv("MLFLOW_TRACKING_URI")
        experiment = os.getenv("MLFLOW_EXPERIMENT")

        # configure mlflow
        mlflow.set_tracking_uri(track)
        mlflow.set_experiment(experiment_name=experiment)

        with mlflow.start_run(run_name=str(os.getenv("MODEL"))):

            # STEP 1: push parameters to mlflow
            mlflow.log_params(params)

            # STEP 2: push metrics to mlflow
            mlflow.log_metrics(metrics)

            # STEP 3: push model to mlflow
            if model:
                mlflow.keras.log_model(model=model,
                            artifact_path="model",
                            keras_module="tensorflow.keras",
                            registered_model_name=str(os.getenv("MODEL")))

        return None

    if os.getenv("MODEL_TARGET") == "local":
        #save model localy
        file_path = os.path.abspath(__file__)
        LOCAL_PATH = os.path.join(os.path.dirname(file_path),"models")
        model_path = os.path.join(LOCAL_PATH,f"{os.getenv('MODEL')}")
        model.save(model_path)


def load_model():
     #Need to add load model from mlflow

    #load model locally"
    file_path = os.path.abspath(__file__)
    LOCAL_PATH = os.path.join(os.path.dirname(file_path),"models")
    model_path = os.path.join(LOCAL_PATH,f"{os.getenv('MODEL')}")
    model = keras.models.load_model(model_path)

    print("Loaded model from local Disk.")

    return model
