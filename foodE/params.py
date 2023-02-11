import os
import time

#MODEL SAVED PATH
timestamp = time.time()
file_path = os.path.abspath(__file__)
LOCAL_PATH = os.path.join(os.path.dirname(file_path),"models")
model_path = os.path.join(LOCAL_PATH,f"{os.getenv('MODEL')}_{timestamp}")
