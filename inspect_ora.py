import os
import sys
import pandas as pd
import requests

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

ORA_URL = "https://media.githubusercontent.com/media/openrepair/data/main/aggregated/202507/OpenRepairData_v0.3_aggregate_202507.csv"
ora_raw_path = os.path.join(DATA_DIR, "ora_aggregate_202507.csv")

def download_file(url, target_path):
    print(f"Downloading from {url} to {target_path}...")
    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(target_path, "wb") as f:
            downloaded = 0
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if downloaded % (10 * 1024 * 1024) < 1024 * 1024:
                        print(f"Downloaded {downloaded / (1024*1024):.1f} MB...")
    print(f"Done! Saved {target_path}")

if not os.path.exists(ora_raw_path):
    download_file(ORA_URL, ora_raw_path)
else:
    print(f"ORA dataset already exists at {ora_raw_path}")

# Filter for Computers / Laptops / IT devices in ORA
# Read in chunks to inspect columns and categories
chunks = pd.read_csv(ora_raw_path, nrows=5000)
print("ORA sample shape:", chunks.shape)
print("ORA columns:", chunks.columns.tolist())
categories = chunks['product_category'].value_counts()
print("Top 10 product categories in first 5000 rows:")
for cat, count in categories.head(10).items():
    print(f"  {cat}: {count}")
