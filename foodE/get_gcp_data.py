
import subprocess
import os


def get_gcp_data():

    bucket_name = os.environ.get('BUCKETNAME')
    filename = os.environ.get('FILENAME')
    #start_byte = 0
    # end_byte = 1048576 # 1 MB

    source = "gs://" + bucket_name + "/" + filename
    destination = "../code/wroby/foodE/raw_data"


    # Use gsutil cp with the -r (range) flag to download a portion of the file
    result = subprocess.run(["gsutil", "cp", "-r","-m",  source, destination], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    #f"{start_byte}-{end_byte}" -> pas sûr de l'ajout ?

    return result
