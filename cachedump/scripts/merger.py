import os
import shutil
from tqdm import tqdm

def merge_folders(input_folders, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through the input folders with a progress bar
    for folder in tqdm(input_folders, desc="Merging folders", unit="folder"):
        # Iterate through the files in each input folder
        for file_name in os.listdir(folder):
            # Create the source and destination file paths
            src_file_path = os.path.join(folder, file_name)
            dest_file_path = os.path.join(output_folder, file_name)

            # Check if the source path is a file
            if os.path.isfile(src_file_path):
                # Copy the file to the output folder
                shutil.copy2(src_file_path, dest_file_path)

# Replace 'path/to/folder1', 'path/to/folder2', and 'path/to/folder3' with the paths to your folders
input_folders = ['../png_files', '../jpg_files', '../jpeg_files']

# Replace 'path/to/merged_folder' with the desired path for the merged folder
output_folder = '../merged_raw'

# Merge the input folders into the output folder
merge_folders(input_folders, output_folder)
