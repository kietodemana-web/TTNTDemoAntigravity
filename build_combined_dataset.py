import os
import sys
import io
import re
import pandas as pd
import numpy as np

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

# Mapping dictionary for the 7 categories from the presentation
# Categories: 'Nguồn', 'Màn hình', 'Quá nhiệt', 'Ổ cứng', 'RAM', 'Mạng', 'Phần mềm'

CATEGORY_PATTERNS = {
    'Nguồn': [
        r'\bbattery\b', r'\bcharger\b', r'\bcharging\b', r'\bpower adapter\b', r'\bpsu\b',
        r'\bpower supply\b', r'\bwon\'?t power\b', r'\bwon\'?t turn on\b', r'\bno power\b',
        r'\bdead battery\b', r'\bpower issue\b', r'\bshutdown abruptly\b', r'\bpower button\b',
        r'\bac adapter\b', r'\bdc jack\b', r'\bcharging port\b', r'\bpowers off\b'
    ],
    'Màn hình': [
        r'\bscreen\b', r'\bdisplay\b', r'\bmonitor\b', r'\bblack screen\b', r'\bblank screen\b',
        r'\bflicker\b', r'\bno display\b', r'\bbacklight\b', r'\blcd\b', r'\bled screen\b',
        r'\bcrack.*screen\b', r'\blines on screen\b', r'\bexternal display\b', r'\bhdmi\b',
        r'\bgraphics card\b', r'\bgpu artifact\b', r'\bdistorted display\b'
    ],
    'Quá nhiệt': [
        r'\boverheat', r'\btemperature\b', r'\bcooling fan\b', r'\bfan noise\b', r'\bloud fan\b',
        r'\bthermal\b', r'\bthermal paste\b', r'\bheatsink\b', r'\bthrottl', r'\bfan not spinning\b',
        r'\bextremely hot\b', r'\bhot to touch\b', r'\bshutting down from heat\b'
    ],
    'Ổ cứng': [
        r'\bhard drive\b', r'\bhdd\b', r'\bssd\b', r'\bdisk drive\b', r'\bstorage\b',
        r'\bbad sector\b', r'\bsmart error\b', r'\bdrive not detected\b', r'\bread/write error\b',
        r'\bdisk full\b', r'\bcorrupt disk\b', r'\bclicking drive\b', r'\bnvme\b', r'\bsata\b'
    ],
    'RAM': [
        r'\bram\b', r'\bmemory\b', r'\bbeep code\b', r'\bbeeping\b', r'\bmemory management\b',
        r'\bdram\b', r'\bdimm\b', r'\bout of memory\b', r'\bmemory leak\b', r'\bbad ram\b',
        r'\bram stick\b', r'\bmemory slot\b'
    ],
    'Mạng': [
        r'\bwi-?fi\b', r'\bnetwork\b', r'\binternet\b', r'\bethernet\b', r'\bdns\b',
        r'\bip address\b', r'\blan\b', r'\brouter\b', r'\bconnectivity\b', r'\bno internet\b',
        r'\bping drop\b', r'\bpacket loss\b', r'\bnetwork adapter\b', r'\bdisconnecting\b'
    ],
    'Phần mềm': [
        r'\bwindows\b', r'\bos\b', r'\boperating system\b', r'\bvirus\b', r'\bmalware\b',
        r'\bblue screen\b', r'\bbsod\b', r'\bdriver\b', r'\bsoftware\b', r'\bapplication\b',
        r'\bboot loop\b', r'\bcrash\b', r'\bfreeze\b', r'\bfrozen\b', r'\bupdate failed\b',
        r'\bransomware\b', r'\bslow performance\b', r'\bmalicious\b'
    ]
}

def classify_text(text):
    if not isinstance(text, str) or not text.strip():
        return None
    text_lower = text.lower()
    
    # Priority scoring
    scores = {}
    for cat, patterns in CATEGORY_PATTERNS.items():
        score = 0
        for pat in patterns:
            matches = len(re.findall(pat, text_lower))
            score += matches
        if score > 0:
            scores[cat] = score
    
    if not scores:
        return None
    # Return category with highest score
    best_cat = max(scores, key=scores.get)
    return best_cat

# Process Hugging Face IT Troubleshooting
df_hf = pd.read_csv('data/hf_it_troubleshooting.csv')
hf_samples = []

for _, row in df_hf.iterrows():
    # Combine issue, symptoms, causes, keywords
    combined_text = f"{row.get('Issue', '')}. {row.get('Symptoms', '')}. {row.get('Common Causes', '')}. {row.get('Keywords', '')}"
    symptoms = str(row.get('Symptoms', '')).strip()
    if not symptoms or symptoms.lower() == 'nan':
        symptoms = str(row.get('Issue', '')).strip()
    
    # Check category
    cat = classify_text(combined_text)
    if cat:
        solution = str(row.get('Solution Steps', '')).strip()
        hf_samples.append({
            'source': 'Hugging Face IT Troubleshooting',
            'id': f"HF_{row.get('ID', '')}",
            'symptoms': symptoms,
            'issue': str(row.get('Issue', '')).strip(),
            'combined_text': combined_text,
            'category': cat,
            'solution': solution,
            'causes': str(row.get('Common Causes', '')).strip()
        })

df_hf_clean = pd.DataFrame(hf_samples)
print(f"Extracted from HF: {len(df_hf_clean)} samples")
print(df_hf_clean['category'].value_counts())

# Process Open Repair Alliance
df_ora = pd.read_csv('data/ora_aggregate_202507.csv', usecols=['id', 'country', 'product_category', 'problem', 'repair_barrier_if_end_of_life', 'repair_status'])
ora_pc = df_ora[df_ora['product_category'].isin(['Laptop', 'Desktop computer', 'Flat screen', 'PC accessory'])].dropna(subset=['problem']).copy()

# German/Dutch/French common terms mapping for ORA repair cafes
ORA_TERM_MAP = {
    'akku': 'battery power',
    'lade': 'charging power charger',
    'strom': 'power electrical',
    'geht nicht an': 'won\'t turn on no power',
    'l?dt nicht': 'not charging power',
    'lauft nicht': 'not working power',
    'bild': 'screen display image',
    'kein bild': 'no display black screen',
    'display': 'screen display',
    'bildschirm': 'screen display monitor',
    'warme': 'thermal overheating hot',
    'w?rme': 'thermal overheating hot',
    'heiss': 'hot overheat',
    'hei?': 'hot overheat',
    'lufter': 'cooling fan noise',
    'l?fter': 'cooling fan noise',
    'festplatte': 'hard drive hdd ssd storage',
    'speicher': 'ram memory storage',
    'absturz': 'crash blue screen bsod',
    'langsam': 'slow freeze performance',
    'wlan': 'wifi network connectivity'
}

ora_samples = []
for _, row in ora_pc.iterrows():
    prob_raw = str(row['problem']).strip()
    if len(prob_raw) < 5:
        continue
    
    # Translate common non-English keywords for detection
    prob_expanded = prob_raw.lower()
    for de_term, en_term in ORA_TERM_MAP.items():
        prob_expanded = prob_expanded.replace(de_term, en_term)
    
    cat = classify_text(prob_expanded)
    if cat:
        # If product_category is Flat screen and cat is not identified, it's Màn hình
        ora_samples.append({
            'source': 'Open Repair Alliance (ORDS)',
            'id': f"ORA_{row['id']}",
            'symptoms': prob_raw,
            'issue': f"{row['product_category']} repair issue",
            'combined_text': f"{row['product_category']}: {prob_raw}",
            'category': cat,
            'solution': str(row.get('repair_status', 'Repair attempted at community repair event')),
            'causes': str(row.get('repair_barrier_if_end_of_life', 'Hardware wear / component failure'))
        })

df_ora_clean = pd.DataFrame(ora_samples)
print(f"\nExtracted from ORA: {len(df_ora_clean)} samples")
print(df_ora_clean['category'].value_counts())

# Combine both datasets
df_total = pd.concat([df_hf_clean, df_ora_clean], ignore_index=True)
print(f"\n==========================================")
print(f"TOTAL REAL DATASET SAMPLES: {len(df_total)}")
print(f"==========================================")
print(df_total['category'].value_counts())
print("\nSamples by source:")
print(df_total['source'].value_counts())
