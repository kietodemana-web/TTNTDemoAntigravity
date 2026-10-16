import sys
import io
import requests

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from fastapi.testclient import TestClient
from server import app

client = TestClient(app)

print("--- Testing /api/benchmark ---")
r = client.get("/api/benchmark")
assert r.status_code == 200
data = r.json()
print("Dataset total samples:", data['dataset_info']['total_samples'])
print("Naive Bayes Accuracy:", data['models']['Naive Bayes (MultinomialNB)']['accuracy'])
print("Naive Bayes Top-3 Accuracy:", data['models']['Naive Bayes (MultinomialNB)']['top3_accuracy'])

print("\n--- Testing /api/diagnose with Slide 11 example ---")
# Slide 11: "Bật máy không lên hình, nghe tiếng bíp. Người dùng chọn: không có hình; có tiếng bíp; máy vẫn có nguồn."
payload = {
    "symptoms": "Bật máy không lên hình, nghe tiếng bíp",
    "selected_tags": ["Có tiếng bíp bíp liên tục khi bật máy", "Không lên hình / màn hình đen xì"]
}
r2 = client.post("/api/diagnose", json=payload)
assert r2.status_code == 200
diag = r2.json()
print("Inference time:", diag['inference_time_ms'], "ms")
print("Top 3 Predictions:")
for p in diag['top_predictions']:
    print(f" Rank {p['rank']}: {p['category']} ({p['probability']}%) - {p['description'][:40]}...")
    for sc in p['sub_causes']:
        print(f"   -> {sc['name']} ({sc['probability']}%)")

print("\n--- Testing /api/dataset-samples ---")
r3 = client.get("/api/dataset-samples?page=1&page_size=3")
assert r3.status_code == 200
samples = r3.json()
print("Total dataset samples accessible via API:", samples['total'])
print("First sample ID:", samples['samples'][0]['sample_id'])

print("\nAll API tests PASSED successfully!")
