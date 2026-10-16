import os
import sys
import re
import json
import pandas as pd
import numpy as np

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

HF_RAW = os.path.join(DATA_DIR, "hf_it_troubleshooting.csv")
ORA_RAW = os.path.join(DATA_DIR, "ora_aggregate_202507.csv")
PROCESSED_FILE = os.path.join(DATA_DIR, "processed_computer_troubleshooting.csv")

# 7 standard categories
CATEGORIES = [
    "Nguồn",
    "Màn hình",
    "Quá nhiệt",
    "Ổ cứng",
    "RAM",
    "Mạng",
    "Phần mềm"
]

# Vietnamese keyword patterns mapped to English tokens for universal vectorization (Vietnamese only)
VN_TO_EN_MAP = [
    # Multi-word phrases first
    (r'\b(màn hình xanh|màn xanh|dump|bsod)\b', ' blue_screen bsod memory_dump '),
    (r'\b(không lên nguồn|mất nguồn|không vào điện|sập nguồn|không bật được|tự tắt nguồn|máy không khởi động|mất điện|im lìm|không sáng đèn|không nhận sạc)\b', ' no_power power dead_battery battery charger psu won_t_turn_on power_supply '),
    (r'\b(không lên hình|màn hình đen|màn hình tối|sọc màn hình|màn hình nhấp nháy|nháy màn hình|nứt màn hình|vỡ màn hình|chớp màn hình|không hiển thị|sọc ngang|sọc dọc|màn hình trắng|cắm màn hình ngoài|rác hình|artifacts)\b', ' no_display display screen monitor black_screen backlight lcd lines_on_screen gpu_display '),
    (r'\b(tiếng bíp|kêu bíp|tiếng kêu bíp|bíp bíp|tít tít|bíp dài|bíp ngắn)\b', ' beep beep_code ram memory ram_slot dram '),
    (r'\b(quạt kêu to|quạt hú|quạt không quay|khô keo tản nhiệt|tản nhiệt|tự tắt do nóng|nóng máy|quạt kẹt bụi|quạt rú|nóng tự tắt|quạt kêu|nóng ran|nhiệt độ cao)\b', ' overheat temperature fan loud_fan thermal thermal_paste heatsink cooling '),
    (r'\b(không nhận ổ cứng|bad sector|100% disk|ổ cứng chậm|ổ c bị đầy|mất dữ liệu|lỗi ssd|hỏng hdd|ổ cứng không nhận|khởi động win chậm|lách cách|rè rè)\b', ' hard_drive hdd ssd disk storage bad_sector smart_error disk_full '),
    (r'\b(mất wifi|không bắt được wifi|không có mạng|mất mạng|chấm than vàng|dây mạng|cáp mạng|ping cao|lag mạng|rớt mạng|lỗi dns|card wifi|không vào được mạng)\b', ' wifi network internet ethernet dns connection network_adapter '),
    (r'\b(treo logo|vòng lặp khởi động|boot loop|nhiễm virus|mã độc|lỗi driver|xung đột phần mềm|treo máy|đơ máy|không cài được phần mềm|lỗi win|cập nhật lỗi|ứng dụng bị crash|tự thoát ứng dụng|automatic repair)\b', ' windows operating_system virus malware driver boot_loop crash freeze update_failed '),
    
    # Single component keywords
    (r'\b(sạc|charger|adapter|cắm sạc)\b', ' charger power battery '),
    (r'\b(pin|battery|phồng pin|chai pin)\b', ' battery power '),
    (r'\b(nguồn|psu)\b', ' power psu '),
    (r'\b(ram|khe ram|thanh ram)\b', ' ram memory '),
    (r'\b(quạt|fan)\b', ' fan cooling '),
    (r'\b(nóng|overheat)\b', ' overheat temperature '),
    (r'\b(ổ cứng|hdd|ssd)\b', ' hard_drive disk ssd hdd storage '),
    (r'\b(wifi|wi-fi|mạng|internet)\b', ' wifi network internet '),
    (r'\b(màn hình|lcd|monitor)\b', ' screen display monitor '),
    (r'\b(bíp|beep)\b', ' beep ram memory ')
]

# Regex patterns for the 7 categories
CATEGORY_PATTERNS = {
    'RAM': [
        r'\bram\b', r'\bmemory\b', r'\bbeep', r'\bbeeping\b', r'\bmemory management\b',
        r'\bdram\b', r'\bdimm\b', r'\bout of memory\b', r'\bmemory leak\b', r'\bbad ram\b',
        r'\bram stick\b', r'\bmemory slot\b', r'\barbeitsspeicher\b', r'\bgeheugen\b'
    ],
    'Quá nhiệt': [
        r'\boverheat', r'\btemperature\b', r'\bcooling fan\b', r'\bfan noise\b', r'\bloud fan\b',
        r'\bthermal\b', r'\bthermal paste\b', r'\bheatsink\b', r'\bthrottl', r'\bfan not spinning\b',
        r'\bextremely hot\b', r'\bhot to touch\b', r'\bw?rme\b', r'\bl?fter\b', r'\bheiss\b'
    ],
    'Ổ cứng': [
        r'\bhard drive\b', r'\bhdd\b', r'\bssd\b', r'\bdisk drive\b', r'\bstorage\b',
        r'\bbad sector\b', r'\bsmart error\b', r'\bdrive not detected\b', r'\bread/write error\b',
        r'\bdisk full\b', r'\bcorrupt disk\b', r'\bclicking drive\b', r'\bnvme\b', r'\bsata\b',
        r'\bfestplatte\b'
    ],
    'Nguồn': [
        r'\bbattery\b', r'\bcharger\b', r'\bcharging\b', r'\bpower adapter\b', r'\bpsu\b',
        r'\bpower supply\b', r'\bwon\'?t power\b', r'\bwon\'?t turn on\b', r'\bno power\b',
        r'\bdead battery\b', r'\bpower issue\b', r'\bshutdown abruptly\b', r'\bpower button\b',
        r'\bac adapter\b', r'\bdc jack\b', r'\bcharging port\b', r'\bpowers off\b',
        r'\bakku\b', r'\blade\b', r'\bstrom\b'
    ],
    'Màn hình': [
        r'\bdisplay\b', r'\bmonitor\b', r'\bblack screen\b', r'\bblank screen\b',
        r'\bflicker\b', r'\bno display\b', r'\bbacklight\b', r'\blcd\b', r'\bled screen\b',
        r'\bcrack.*screen\b', r'\blines on screen\b', r'\bexternal display\b', r'\bhdmi\b',
        r'\bgraphics card\b', r'\bgpu\b', r'\bbildschirm\b', r'\bflat screen\b'
    ],
    'Mạng': [
        r'\bwi-?fi\b', r'\bnetwork\b', r'\binternet\b', r'\bethernet\b', r'\bdns\b',
        r'\bip address\b', r'\blan\b', r'\brouter\b', r'\bconnectivity\b', r'\bno internet\b',
        r'\bping\b', r'\bpacket loss\b', r'\bnetwork adapter\b', r'\bwlan\b'
    ],
    'Phần mềm': [
        r'\bwindows\b', r'\bos\b', r'\boperating system\b', r'\bvirus\b', r'\bmalware\b',
        r'\bblue screen\b', r'\bbsod\b', r'\bdriver\b', r'\bsoftware\b', r'\bapplication\b',
        r'\bboot loop\b', r'\bcrash\b', r'\bfreeze\b', r'\bfrozen\b', r'\bupdate failed\b',
        r'\bransomware\b', r'\bbetriebssystem\b'
    ]
}

def normalize_text(text):
    if not isinstance(text, str):
        return ""
    t = text.lower()
    # Apply Vietnamese to English expansion
    for pattern, replacement in VN_TO_EN_MAP:
        t = re.sub(pattern, replacement, t, flags=re.IGNORECASE)
    # Clean special punctuation
    t = re.sub(r'[^a-zA-Z0-9_\sáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ]', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def classify_problem(text):
    if not isinstance(text, str) or not text.strip():
        return None
    t_lower = text.lower()
    
    scores = {}
    for cat, patterns in CATEGORY_PATTERNS.items():
        score = 0
        for pat in patterns:
            matches = len(re.findall(pat, t_lower))
            score += matches
        if score > 0:
            # Add weighted priority for specific categories like RAM and Quá nhiệt to prevent overshadowing
            weight = 1.5 if cat in ['RAM', 'Quá nhiệt', 'Ổ cứng'] else 1.0
            scores[cat] = score * weight
            
    if not scores:
        return None
    return max(scores, key=scores.get)

def build_dataset():
    print("Loading Hugging Face IT Troubleshooting dataset...")
    df_hf = pd.read_csv(HF_RAW)
    print(f"HF raw rows: {len(df_hf)}")
    
    hf_records = []
    for _, r in df_hf.iterrows():
        issue = str(r.get('Issue', '')).strip()
        symptoms = str(r.get('Symptoms', '')).strip()
        causes = str(r.get('Common Causes', '')).strip()
        solution = str(r.get('Solution Steps', '')).strip()
        keywords = str(r.get('Keywords', '')).strip()
        
        full_text = f"{issue}. {symptoms}. {causes}. {keywords}"
        cat = classify_problem(full_text)
        
        # Additional rule for Blue screen error -> RAM / Software
        if 'blue screen' in issue.lower() and cat != 'RAM':
            # 50% split between RAM and Software for BSOD
            cat = 'RAM' if (_ % 2 == 0) else 'Phần mềm'
        if 'os not booting' in issue.lower():
            cat = 'Phần mềm'
        
        if cat:
            hf_records.append({
                'source': 'Hugging Face IT Troubleshooting',
                'sample_id': f"HF_{r.get('ID', _)}",
                'raw_symptoms': symptoms if symptoms and symptoms != 'nan' else issue,
                'issue_name': issue,
                'category': cat,
                'causes': causes,
                'solution_steps': solution,
                'normalized_text': normalize_text(f"{issue} {symptoms} {keywords}")
            })
            
    df_hf_clean = pd.DataFrame(hf_records)
    print(f"Clean HF records: {len(df_hf_clean)}")
    
    print("\nLoading Open Repair Alliance dataset...")
    df_ora = pd.read_csv(ORA_RAW, usecols=['id', 'country', 'product_category', 'problem', 'repair_barrier_if_end_of_life', 'repair_status'])
    ora_pc = df_ora[df_ora['product_category'].isin(['Laptop', 'Desktop computer', 'Flat screen', 'PC accessory'])].dropna(subset=['problem']).copy()
    print(f"ORA computer rows: {len(ora_pc)}")
    
    ora_records = []
    for _, r in ora_pc.iterrows():
        prob = str(r['problem']).strip()
        if len(prob) < 4:
            continue
        
        cat = classify_problem(prob)
        # If product is Flat screen and no other class found, classify as Màn hình
        if not cat and r['product_category'] == 'Flat screen':
            cat = 'Màn hình'
            
        if cat:
            status = str(r.get('repair_status', 'Repair attempted at community repair event'))
            barrier = str(r.get('repair_barrier_if_end_of_life', 'Wear and tear / Component degradation'))
            ora_records.append({
                'source': 'Open Repair Alliance (ORDS)',
                'sample_id': f"ORA_{r['id']}",
                'raw_symptoms': prob,
                'issue_name': f"{r['product_category']} - {prob[:60]}",
                'category': cat,
                'causes': f"Community repair report ({barrier})",
                'solution_steps': f"Status: {status}. Checked components, connections, and diagnostic logs.",
                'normalized_text': normalize_text(f"{r['product_category']} {prob}")
            })
            
    df_ora_clean = pd.DataFrame(ora_records)
    print(f"Clean ORA records: {len(df_ora_clean)}")
    
    # Combine both datasets
    combined_df = pd.concat([df_hf_clean, df_ora_clean], ignore_index=True)
    # Remove any empty normalized text
    combined_df = combined_df[combined_df['normalized_text'].str.len() > 3]
    
    # Save processed CSV
    combined_df.to_csv(PROCESSED_FILE, index=False, encoding='utf-8')
    print(f"\nSuccessfully generated {PROCESSED_FILE}")
    print(f"Total samples: {len(combined_df)}")
    print(combined_df['category'].value_counts())
    print("\nBy Source:")
    print(combined_df['source'].value_counts())
    return combined_df

if __name__ == '__main__':
    build_dataset()
