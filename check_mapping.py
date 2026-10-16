import os
import re
import pandas as pd
import numpy as np

# Load HF dataset
df_hf = pd.read_csv('data/hf_it_troubleshooting.csv')
print(f"HF raw count: {len(df_hf)}")

# Load ORA dataset
df_ora = pd.read_csv('data/ora_aggregate_202507.csv', usecols=['id', 'country', 'product_category', 'problem', 'repair_barrier_if_end_of_life', 'repair_status'])
ora_pc = df_ora[df_ora['product_category'].isin(['Laptop', 'Desktop computer', 'Flat screen', 'PC accessory'])].dropna(subset=['problem']).copy()
print(f"ORA PC raw count: {len(ora_pc)}")

# Let's inspect HF unique Issues and Categories
print("\nHF Category counts:")
print(df_hf['Category'].value_counts())

# Check how many rows in HF have keywords matching our 7 classes
keywords_map = {
    'Nguồn': [r'\bpower\b', r'\bbattery\b', r'\bcharger\b', r'\bcharging\b', r'\bpsu\b', r'\bturn on\b', r'\bwon\'?t power\b', r'\bpower supply\b', r'\badapter\b', r'\bwon\'?t start\b', r'\bno power\b', r'\bshuts? down abruptly\b'],
    'Màn hình': [r'\bscreen\b', r'\bdisplay\b', r'\bmonitor\b', r'\bblack screen\b', r'\bblank screen\b', r'\bflicker\b', r'\bno display\b', r'\bbacklight\b', r'\bresolution\b', r'\bhdmi\b', r'\bgpu\b', r'\bgraphics card\b', r'\blcd\b'],
    'Quá nhiệt': [r'\boverheat', r'\btemperature\b', r'\bfan\b', r'\bthermal\b', r'\bcooling\b', r'\bheat\b', r'\bthermal paste\b', r'\bloud fan\b', r'\bthrottl'],
    'Ổ cứng': [r'\bhard drive\b', r'\bhdd\b', r'\bssd\b', r'\bdisk\b', r'\bstorage\b', r'\bbad sector\b', r'\bsmart error\b', r'\bdrive not detected\b', r'\bread error\b', r'\bwrite error\b', r'\bcorrupt disk\b'],
    'RAM': [r'\bram\b', r'\bmemory\b', r'\bbeep\b', r'\bbeep code\b', r'\bmemory management\b', r'\bdram\b', r'\bdimm\b', r'\bout of memory\b'],
    'Mạng': [r'\bnetwork\b', r'\bwi-?fi\b', r'\binternet\b', r'\bethernet\b', r'\bdns\b', r'\bip address\b', r'\bconnection\b', r'\brouter\b', r'\blan\b', r'\bconnectivity\b'],
    'Phần mềm': [r'\bwindows\b', r'\bos\b', r'\boperating system\b', r'\bvirus\b', r'\bmalware\b', r'\bbusy loop\b', r'\bboot loop\b', r'\bblue screen\b', r'\bbsod\b', r'\bdriver\b', r'\bsoftware\b', r'\bapplication\b', r'\bupdate failed\b', r'\bcrash\b', r'\bfrozen\b', r'\bfreeze\b']
}

print("\nKeywords mapping defined.")
