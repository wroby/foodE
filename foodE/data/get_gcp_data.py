
import subprocess
import os


def get_gcp_data():

    bucket_name = os.environ.get('BUCKETNAME')
    filename = os.environ.get('FILENAME')

    source = "gs://" + bucket_name + "/" + filename
    print(source)

    if os.environ.get("DESTINATION") == "local":
        file_path = os.path.abspath(__file__)
        grandparent_folder = os.path.dirname(os.path.dirname(os.path.dirname(file_path)))
        destination = os.path.join(grandparent_folder, "raw_data/")
        print(destination)
    elif os.environ.get("DESTINATION") == "cloud":
        os.mkdir("/FoodE/raw_data")
        destination = "./FoodE/raw_data/"
    else: print("No source selected")



    # Use gsutil cp with the -r (range) flag to download a portion of the file
    result = subprocess.run(["gsutil" ,"-m","cp", "-r",  source, destination])
    print(result)
    return result
