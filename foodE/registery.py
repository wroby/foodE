import mlflow
from mlflow.tracking import MlflowClient
import time
import os
import numpy as np
import matplotlib.pyplot as plt
import mlflow.keras
from sklearn.metrics import confusion_matrix, classification_report
from tensorflow.keras.models import load_model

timestamp = time.time()
file_path = os.path.abspath(__file__)
LOCAL_PATH = os.path.join(os.path.dirname(file_path),"models")
model_path = os.path.join(LOCAL_PATH,f"{os.getenv('MODEL')}_{timestamp}")

def save_model(model = None, 
               params: dict = None,
               metrics: dict = None,) -> None:
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
    model.save(os.path.join(model_path,"model"))

def save_confusion_matrix(model,test):
    global true_label, predict_label
    true_label = []
    predict_label = []

    for images,labels in test:
        true_label.extend(np.argmax(labels,axis=1).tolist())
        predict = model.predict(images)
        predict_label.extend(np.argmax(predict,axis=1).tolist())
    true_label = np.array(true_label)
    predict_label = np.array(predict_label)

    cm = confusion_matrix(true_label, predict_label)

    fig = plt.figure()
    plt.matshow(cm, cmap=plt.cm.Blues)
    plt.title("Confusion matrix")
    plt.ylabel("True labels")
    plt.xlabel("Predict label")
    plt.savefig(os.path.join(model_path,"confusion_matrix"))

def save_plot(history):
    fig ,axes = plt.subplots(1,2,figsize=(20,5))

    #Accuracy plot
    axes[0].plot(history.history['accuracy'])
    axes[0].plot(history.history['val_accuracy'])
    axes[0].set_title('model accuracy')
    axes[0].set_ylabel('accuracy')
    axes[0].set_xlabel('epoch')
    axes[0].legend(['train', 'test'], loc='upper left')

    #Loss plot
    axes[1].plot(history.history['loss'])
    axes[1].plot(history.history['val_loss'])
    axes[1].set_title('model loss')
    axes[1].set_ylabel('loss')
    axes[1].set_xlabel('epoch')
    axes[1].legend(['train', 'test'], loc='upper right')

    fig.savefig(os.path.join(model_path,"history"))

def save_classification_report():
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)),"raw_data/food-101/food-101-test/images")
    report = classification_report(true_label,predict_label,\
            target_names= [x for x in os.listdir(path) if os.path.isdir(os.path.join(path,x))])
    with open(os.path.join(model_path,"report"),"w") as file:
        file.write(report)

def model_load():
    #Need to add load model from mlflow

    #load model locally"
    time = os.getenv("TIMESTAMP_MODEL")
    file_path = os.path.abspath(__file__)
    LOCAL_PATH = os.path.join(os.path.dirname(file_path),"models")
    model_path = os.path.join(LOCAL_PATH,f"{os.getenv('MODEL')}_{time}")
    print(model_path)
    model = load_model(os.path.join(model_path,"model"))
    #model = load_model(model_path)
    print("Loaded model from local Disk.")

    return model
