
import subprocess
import os


def get_gcp_data():

    bucket_name = os.environ.get('BUCKETNAME')
    filename = os.environ.get('FILENAME')

    source = "gs://" + bucket_name + "/" + filename
    print(f"source OK: {source}")

    file_path = os.path.abspath(__file__)
    grandparent_folder = os.path.dirname(os.path.dirname(file_path))
    raw_data_folder = os.path.join(grandparent_folder, "raw_data")


    if os.environ.get("DESTINATION") == "local":
        destination = raw_data_folder
        print(f"destination OK: {raw_data_folder}")
    elif os.environ.get("DESTINATION") == "cloud":
        os.mkdir("/FoodE/raw_data")
        destination = raw_data_folder
    else: print("No source selected")


    # Use gsutil cp with the -r (range) flag to download a portion of the file
    result = subprocess.run(["gsutil", "cp", "-r", "-m", source, destination])

    return result
