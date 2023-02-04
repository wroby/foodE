
import subprocess
import os


def get_gcp_data():

    bucket_name = os.environ.get('BUCKETNAME')
    filename = os.environ.get('FILENAME')

    source = "gs://" + bucket_name + "/" + filename
    
    if os.environ.get("DESTINATION") == "local":
        destination = "../code/wroby/foodE/raw_data/food-101"
    elif os.environ.get("DESTINATION") == "cloud":
        os.mkdir("/FoodE/raw_data")
        destination = "./FoodE/raw_data"
    else: print("No source selected")


    # Use gsutil cp with the -r (range) flag to download a portion of the file
    result = subprocess.run(["gsutil", "cp", "-r","-m",  source, destination], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return result
