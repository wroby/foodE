import mlflow
from mlflow.tracking import MlflowClient
import time
import os
import matplotlib.pyplot as plt
import mlflow.keras
from tensorflow import keras



def save_model(model: keras.Model = None,
               params: dict = None,
               metrics: dict = None,
               history = None,
               cm = None,
               report = None) -> None:
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
            # if model:
            #     mlflow.keras.log_model(model=model,
            #                 artifact_path="model",
            #                 #keras_module="tensorflow.keras",
            #                 registered_model_name=str(os.getenv("MODEL")))


    #save model localy
    timestamp = time.time()
    file_path = os.path.abspath(__file__)
    LOCAL_PATH = os.path.join(os.path.dirname(file_path),"models")
    model_path = os.path.join(LOCAL_PATH,f"{os.getenv('MODEL')}_{timestamp}")
    model.save(os.path.join(model_path,"model"))

    #Plot history
    fig ,axes = plt.subplots(1,2,figsize=(20,5))
    axes[0].plot(history.history['accuracy'])
    axes[0].plot(history.history['val_accuracy'])
    axes[0].set_title('model accuracy')
    axes[0].set_ylabel('accuracy')
    axes[0].set_xlabel('epoch')
    axes[0].legend(['train', 'test'], loc='upper left')

    axes[1].plot(history.history['loss'])
    axes[1].plot(history.history['val_loss'])
    axes[1].set_title('model loss')
    axes[1].set_ylabel('loss')
    axes[1].set_xlabel('epoch')
    axes[1].legend(['train', 'test'], loc='upper right')

    fig.savefig(os.path.join(model_path,"history"))

    #save confusion matrix
    fig = plt.figure()
    plt.matshow(cm, cmap=plt.cm.Blues)
    plt.title("Confusion matrix")
    plt.ylabel("True labels")
    plt.xlabel("Predict label")
    plt.savefig(os.path.join(model_path,"confusion_matrix"))

    #save report
    with open(os.path.join(model_path,"report"),"w") as file:
        file.write(report)

def load_model():
    #Need to add load model from mlflow

    #load model locally"
    time = os.getenv("TIMESTAMP_MODEL")
    file_path = os.path.abspath(__file__)
    LOCAL_PATH = os.path.join(os.path.dirname(file_path),"models")
    model_path = os.path.join(LOCAL_PATH,f"{os.getenv('MODEL')}_{time}")
    model = keras.models.load_model(model_path)
    print("Loaded model from local Disk.")

    return model
