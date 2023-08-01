#!/usr/bin/env python3

import os
import requests
import hashlib
from tqdm import tqdm

# Function to download a file with a progress bar
def download_file(url, filename):
    response = requests.get(url, stream=True)
    total = int(response.headers.get('content-length', 0))
    with open(filename, 'wb') as file, tqdm(
            desc=filename,
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)

print("Enter the URL: ")
presigned_url = input()

print("\nEnter the list of models to download without spaces (7B,13B,70B,7B-chat,13B-chat,70B-chat), or press Enter for all: ")
model_size = input()
target_folder = "."  # where all files should end up
os.makedirs(target_folder, exist_ok=True)

if model_size == "":
    model_size = "7B,13B,70B,7B-chat,13B-chat,70B-chat"

print("\nDownloading LICENSE and Acceptable Usage Policy")
download_file(presigned_url.replace('*', "LICENSE"), os.path.join(target_folder, "LICENSE"))
download_file(presigned_url.replace('*', "USE_POLICY.md"), os.path.join(target_folder, "USE_POLICY.md"))

print("\nDownloading tokenizer")
download_file(presigned_url.replace('*', "tokenizer.model"), os.path.join(target_folder, "tokenizer.model"))
download_file(presigned_url.replace('*', "tokenizer_checklist.chk"), os.path.join(target_folder, "tokenizer_checklist.chk"))

for model in model_size.split(","):
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
        
    print(f"\nDownloading {model_path}")
    os.makedirs(os.path.join(target_folder, model_path), exist_ok=True)

    for s in range(shard + 1):
        download_file(presigned_url.replace('*', f"{model_path}/consolidated.{str(s).zfill(2)}.pth"), os.path.join(target_folder, model_path, f"consolidated.{str(s).zfill(2)}.pth"))

    download_file(presigned_url.replace('*', f"{model_path}/params.json"), os.path.join(target_folder, model_path, "params.json"))
    download_file(presigned_url.replace('*', f"{model_path}/checklist.chk"), os.path.join(target_folder, model_path, "checklist.chk"))

