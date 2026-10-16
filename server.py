import os
import sys
import time
import json
import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional

# Ensure UTF-8
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

from data_pipeline import normalize_text, CATEGORIES
from knowledge_base import DIAGNOSTIC_KNOWLEDGE

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
DATA_FILE = os.path.join(BASE_DIR, "data", "processed_computer_troubleshooting.csv")

app = FastAPI(
    title="Hệ thống Chẩn đoán Sự cố Máy tính - Naive Bayes",
    description="Hệ thống tư vấn dựa trên triệu chứng sử dụng bộ phân lớp Naive Bayes trên dữ liệu thật Open Repair Alliance & Hugging Face",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Model & Vectorizer
print("Loading Naive Bayes model and Vectorizer...")
nb_model = joblib.load(os.path.join(MODEL_DIR, "naive_bayes_model.joblib"))
vectorizer = joblib.load(os.path.join(MODEL_DIR, "vectorizer.joblib"))

# Load Benchmark Results
with open(os.path.join(MODEL_DIR, "benchmark_results.json"), "r", encoding="utf-8") as f:
    BENCHMARK_DATA = json.load(f)

# Load dataset for exploration (keep key columns in memory for fast search)
print("Loading dataset for exploration...")
df_samples = pd.read_csv(DATA_FILE)
print(f"Loaded {len(df_samples)} samples.")

class DiagnosisRequest(BaseModel):
    symptoms: str
    selected_tags: Optional[List[str]] = []

@app.get("/api/benchmark")
def get_benchmark():
    return BENCHMARK_DATA

@app.get("/api/symptom-tags")
def get_symptom_tags():
    return [
        {"id": "no_power", "label": "Bật không lên nguồn / hoàn toàn im lìm", "category": "Nguồn"},
        {"id": "battery_drain", "label": "Pin chai nhanh / sập ngay khi rút sạc", "category": "Nguồn"},
        {"id": "charger_loose", "label": "Cắm sạc không báo đèn / lúc nhận lúc không", "category": "Nguồn"},
        {"id": "black_screen", "label": "Không lên hình / màn hình đen xì", "category": "Màn hình"},
        {"id": "screen_lines", "label": "Màn hình bị sọc ngang, sọc dọc / giật hình", "category": "Màn hình"},
        {"id": "screen_flicker", "label": "Màn hình chớp nháy khi gập mở góc máy", "category": "Màn hình"},
        {"id": "overheating", "label": "Máy rất nóng / nhiệt độ CPU > 90°C", "category": "Quá nhiệt"},
        {"id": "loud_fan", "label": "Quạt tản nhiệt kêu to / rú liên tục", "category": "Quá nhiệt"},
        {"id": "fan_error", "label": "Máy báo lỗi Fan Error / quạt không quay", "category": "Quá nhiệt"},
        {"id": "slow_disk", "label": "Task Manager báo 100% Disk / đơ đĩa", "category": "Ổ cứng"},
        {"id": "hdd_clicking", "label": "Ổ cứng kêu rè rè / lách cách cơ học", "category": "Ổ cứng"},
        {"id": "bad_sector", "label": "Khởi động cực chậm / tự chạy Scan disk", "category": "Ổ cứng"},
        {"id": "beep_sound", "label": "Có tiếng bíp bíp liên tục khi bật máy", "category": "RAM"},
        {"id": "ram_unseated", "label": "Quạt quay, máy sáng đèn nhưng không lên hình", "category": "RAM"},
        {"id": "bsod_ram", "label": "Màn hình xanh lỗi MEMORY_MANAGEMENT", "category": "RAM"},
        {"id": "no_wifi", "label": "Mất biểu tượng Wi-Fi / không quét được mạng", "category": "Mạng"},
        {"id": "yellow_warning", "label": "Mạng báo Connected nhưng chấm than vàng", "category": "Mạng"},
        {"id": "ping_spike", "label": "Ping cao bất thường / rớt gói tin gián đoạn", "category": "Mạng"},
        {"id": "bsod_software", "label": "Màn hình xanh BSOD tự khởi động lại máy", "category": "Phần mềm"},
        {"id": "boot_loop", "label": "Treo logo Windows / Automatic Repair loop", "category": "Phần mềm"},
        {"id": "virus_malware", "label": "Nghi máy dính virus đào coin / CPU luôn 100%", "category": "Phần mềm"}
    ]

@app.post("/api/diagnose")
def diagnose_issue(req: DiagnosisRequest):
    t_start = time.time()
    
    # Combine free text symptoms and selected tag labels
    combined_query = req.symptoms.strip()
    if req.selected_tags:
        combined_query += " " + " ".join(req.selected_tags)
        
    if not combined_query.strip():
        raise HTTPException(status_code=400, detail="Vui lòng nhập triệu chứng hoặc chọn các biểu hiện sự cố.")
        
    # Normalize query (expand Vietnamese symptom expressions to diagnostic tokens)
    normalized = normalize_text(combined_query)
    
    # Transform with TF-IDF Vectorizer
    vec_input = vectorizer.transform([normalized])
    
    # Predict probabilities via Naive Bayes
    probs = nb_model.predict_proba(vec_input)[0]
    classes = list(nb_model.classes_)
    
    # Sort classes by descending probability
    sorted_indices = np.argsort(probs)[::-1]
    
    all_probabilities = {}
    for idx in sorted_indices:
        cat_name = classes[idx]
        all_probabilities[cat_name] = round(float(probs[idx]) * 100, 2)
        
    # Get Top-3 categories (Slide 6 & Slide 11)
    top_indices = sorted_indices[:3]
    top_predictions = []
    
    # Calculate relative weights among top 3 for sub-cause display
    top_prob_sum = sum([probs[i] for i in top_indices])
    
    for rank, idx in enumerate(top_indices, 1):
        cat = classes[idx]
        raw_prob = float(probs[idx])
        prob_pct = round(raw_prob * 100, 2)
        
        info = DIAGNOSTIC_KNOWLEDGE.get(cat, {})
        
        # Format sub causes with scaled probabilities
        sub_causes = []
        for sc in info.get("sub_causes", []):
            scaled_sub_prob = round(prob_pct * sc["prob_factor"], 1)
            sub_causes.append({
                "name": sc["name"],
                "probability": scaled_sub_prob,
                "symptoms": sc["symptoms"],
                "action": sc["action"]
            })
            
        top_predictions.append({
            "rank": rank,
            "category": cat,
            "probability": prob_pct,
            "icon": info.get("icon", "🔧"),
            "color": info.get("color", "#64748b"),
            "description": info.get("description", ""),
            "sub_causes": sub_causes,
            "safety_steps": info.get("safety_steps", []),
            "resolution_steps": info.get("resolution_steps", [])
        })
        
    inference_time = round((time.time() - t_start) * 1000, 3)
    
    return {
        "success": True,
        "input_query": combined_query,
        "normalized_tokens": normalized,
        "top_predictions": top_predictions,
        "all_probabilities": all_probabilities,
        "inference_time_ms": inference_time,
        "model_architecture": "Multinomial Naive Bayes (Laplace smoothing α=1.0)",
        "features_extracted": int(vec_input.nnz)
    }

@app.get("/api/dataset-samples")
def get_dataset_samples(
    page: int = Query(1, ge=1),
    page_size: int = Query(15, ge=1, le=100),
    source: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None
):
    df_filtered = df_samples.copy()
    
    if source and source != "All":
        df_filtered = df_filtered[df_filtered['source'] == source]
        
    if category and category != "All":
        df_filtered = df_filtered[df_filtered['category'] == category]
        
    if search:
        search_lower = search.lower()
        mask = (
            df_filtered['raw_symptoms'].astype(str).str.lower().str.contains(search_lower, na=False) |
            df_filtered['issue_name'].astype(str).str.lower().str.contains(search_lower, na=False) |
            df_filtered['causes'].astype(str).str.lower().str.contains(search_lower, na=False) |
            df_filtered['sample_id'].astype(str).str.lower().str.contains(search_lower, na=False)
        )
        df_filtered = df_filtered[mask]
        
    total_count = len(df_filtered)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    
    records = df_filtered.iloc[start_idx:end_idx].to_dict(orient="records")
    
    return {
        "total": total_count,
        "page": page,
        "page_size": page_size,
        "total_pages": int(np.ceil(total_count / page_size)),
        "samples": records
    }

# Mount static files
STATIC_DIR = os.path.join(BASE_DIR, "static")
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def serve_index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
