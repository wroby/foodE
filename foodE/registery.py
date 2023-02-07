import mlflow
from mlflow.tracking import MlflowClient

import os


from tensorflow import keras


def save_model(model: keras.Model = None,
               params: dict = None,
               metrics: dict = None) -> None:
    """
    persist trained model, params and metrics
    """

    if os.getenv("MODEL_TARGET") == "mlflow":

        # retrieve mlflow env params
        track = os.environ.get("MLFLOW_TRACKING_URI")
        experiment = os.environ.get("MLFLOW_EXPERIMENT")

        # configure mlflow
        mlflow.set_tracking_uri(track)
        mlflow.set_experiment(experiment_name=experiment)

        with mlflow.start_run():

            # STEP 1: push parameters to mlflow
            mlflow.log_params(params)

            # STEP 2: push metrics to mlflow
            mlflow.log_metrics(metrics)

            # STEP 3: push model to mlflow
            if model:
                mlflow.keras.log_model(keras_model=model,
                            artifact_path="model",
                            keras_module="tensorflow.keras",
                            registered_model_name="foodE_model")

        return None
