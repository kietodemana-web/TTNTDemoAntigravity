import os
import io
import csv
import json
import requests
import pandas as pd
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

HF_URL = "https://huggingface.co/datasets/UmerSajid/IT-Troubleshooting-Dataset/raw/main/Enhanced_IT_Troubleshooting_Dataset_with_Links%20.csv"
ORA_URL = "https://media.githubusercontent.com/media/openrepair/data/main/aggregated/202507/OpenRepairData_v0.3_aggregate_202507.csv"

def download_file(url, target_path, max_bytes=None):
    print(f"Downloading from {url} to {target_path}...")
    headers = {}
    if max_bytes:
        headers["Range"] = f"bytes=0-{max_bytes-1}"
    
    response = requests.get(url, headers=headers, stream=True, timeout=60)
    response.raise_for_status()
    with open(target_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=65536):
            if chunk:
                f.write(chunk)
    size_mb = os.path.getsize(target_path) / (1024 * 1024)
    print(f"Saved {target_path} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    hf_raw_path = os.path.join(DATA_DIR, "hf_it_troubleshooting.csv")
    if not os.path.exists(hf_raw_path):
        download_file(HF_URL, hf_raw_path)
    else:
        print(f"Hugging Face dataset already exists at {hf_raw_path}")

    # Inspect HF dataset columns and rows
    df_hf = pd.read_csv(hf_raw_path)
    print("HF Dataset Shape:", df_hf.shape)
    print("HF Columns:", df_hf.columns.tolist())
    print("HF Head 2:\n", df_hf.head(2).to_dict(orient="records"))
