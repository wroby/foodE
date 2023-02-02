import os
import shutil


def renaming_files():
    """Create a new directory with all images rename by their label"""
    os.mkdir("../raw_data/full_images")
    path = r'../raw_data/images'
    new_dir = r'../raw_data/full_images'

    all_files = 0 #Counting files copied

    for folder in os.listdir(path):
        i = 1 #Number added to file

        if os.path.isdir(os.path.join(path,folder)):
            for files in os.listdir(os.path.join(path,folder)):
                #Checking that file is image
                if files.endswith(".jpg"):
                    #Copy file into new dir
                    shutil.copy(os.path.join(path,folder,files),new_dir)
                    new_name = folder + f'{i}.jpg'
                    new_path = os.path.join(new_dir,new_name)

                    #rename file as label + number
                    os.rename(os.path.join(new_dir,files),new_path)

                    i+=1
                    all_files+=1
    print(f'Copied {all_files} files in {new_dir}')

if __name__ == "__main__":
    renaming_files()
