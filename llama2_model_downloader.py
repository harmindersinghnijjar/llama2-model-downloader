#!/usr/bin/env python3

# Import necessary libraries
import os
import requests
import hashlib
from tqdm import tqdm

# Function to download a file with a progress bar
def download_file(url, filename):
    # Send a request to the given URL to get the file
    response = requests.get(url, stream=True)
    # Get the total size of the file from the 'content-length' header
    total = int(response.headers.get('content-length', 0))
    # Open the file in binary write mode
    with open(filename, 'wb') as file, tqdm(
            desc=filename,             # Description for the progress bar
            total=total,               # Total size of the file for the progress bar
            unit='iB',                 # Unit for displaying file size
            unit_scale=True,           # Scale the unit to KB, MB, etc.
            unit_divisor=1024,         # Divisor for scaling the unit
        ) as bar:
        for data in response.iter_content(chunk_size=1024):
            # Write the downloaded chunk to the file
            size = file.write(data)
            # Update the progress bar with the size of the downloaded chunk
            bar.update(size)

# Get the URL from the user
print("Enter the URL: ")
presigned_url = input()

# Get the list of models to download from the user or use default values
print("\nEnter the list of models to download without spaces (7B,13B,70B,7B-chat,13B-chat,70B-chat), or press Enter for all: ")
model_size = input()
target_folder = "."  # where all files should end up
os.makedirs(target_folder, exist_ok=True)

if model_size == "":
    model_size = "7B,13B,70B,7B-chat,13B-chat,70B-chat"

# Download the LICENSE and Acceptable Usage Policy files
print("\nDownloading LICENSE and Acceptable Usage Policy")
download_file(presigned_url.replace('*', "LICENSE"), os.path.join(target_folder, "LICENSE"))
download_file(presigned_url.replace('*', "USE_POLICY.md"), os.path.join(target_folder, "USE_POLICY.md"))

# Download the tokenizer files
print("\nDownloading tokenizer")
download_file(presigned_url.replace('*', "tokenizer.model"), os.path.join(target_folder, "tokenizer.model"))
download_file(presigned_url.replace('*', "tokenizer_checklist.chk"), os.path.join(target_folder, "tokenizer_checklist.chk"))

# Loop through the list of models and download them
for model in model_size.split(","):
    # Determine the shard and model path based on the selected model
    if model == "7B":
        shard = 0
        model_path = "llama-2-7b"
    elif model == "7B-chat":
        shard = 0
        model_path = "llama-2-7b-chat"
    elif model == "13B":
        shard = 1
        model_path = "llama-2-13b"
    elif model == "13B-chat":
        shard = 1
        model_path = "llama-2-13b-chat"
    elif model == "70B":
        shard = 7
        model_path = "llama-2-70b"
    elif model == "70B-chat":
        shard = 7
        model_path = "llama-2-70b-chat"
        
    # Print the model being downloaded
    print(f"\nDownloading {model_path}")
    # Create the folder for the model if it doesn't exist
    os.makedirs(os.path.join(target_folder, model_path), exist_ok=True)

    # Download each shard of the model
    for s in range(shard + 1):
        download_file(presigned_url.replace('*', f"{model_path}/consolidated.{str(s).zfill(2)}.pth"), os.path.join(target_folder, model_path, f"consolidated.{str(s).zfill(2)}.pth"))

    # Download other files related to the model
    download_file(presigned_url.replace('*', f"{model_path}/params.json"), os.path.join(target_folder, model_path, "params.json"))
    download_file(presigned_url.replace('*', f"{model_path}/checklist.chk"), os.path.join(target_folder, model_path, "checklist.chk"))
