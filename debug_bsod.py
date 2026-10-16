import sys, joblib, numpy as np
from data_pipeline import normalize_text

sys.stdout.reconfigure(encoding='utf-8')
vec = joblib.load('models/vectorizer.joblib')
nb = joblib.load('models/naive_bayes_model.joblib')

text = 'Màn hình xanh BSOD liên tục báo lỗi MEMORY_MANAGEMENT khi mở nhiều ứng dụng Màn hình xanh lỗi MEMORY_MANAGEMENT'
norm = normalize_text(text)
print('Normalized:', repr(norm))
v = vec.transform([norm])
words = [w for w, i in vec.vocabulary_.items() if v[0, i] > 0]
print('Features present in query:', words)
for w in words:
    idx = vec.vocabulary_[w]
    probs = [f"{c}:{nb.feature_log_prob_[c_idx][idx]:.2f}" for c_idx, c in enumerate(nb.classes_)]
    print(f"Feature '{w}': " + ", ".join(probs))
