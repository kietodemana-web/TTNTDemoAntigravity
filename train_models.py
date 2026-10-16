import os
import sys
import json
import time
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, classification_report

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "processed_computer_troubleshooting.csv")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(MODEL_DIR, exist_ok=True)

CATEGORIES = [
    "Nguồn",
    "Màn hình",
    "Quá nhiệt",
    "Ổ cứng",
    "RAM",
    "Mạng",
    "Phần mềm"
]

def top_k_accuracy(model, X_test, y_test, k=3):
    probs = model.predict_proba(X_test)
    classes = list(model.classes_)
    top_k_preds = np.argsort(probs, axis=1)[:, -k:]
    correct = 0
    for idx, true_label in enumerate(y_test):
        true_idx = classes.index(true_label)
        if true_idx in top_k_preds[idx]:
            correct += 1
    return correct / len(y_test)

def train_and_evaluate():
    print("Loading processed dataset...")
    df = pd.read_csv(DATA_PATH)
    print(f"Total dataset size: {len(df)} samples")
    
    # Feature and Label
    X = np.array(df['normalized_text'].astype(str).tolist())
    y = np.array(df['category'].astype(str).tolist())
    
    # Stratified 80/20 train/test split (Slide 7 & 8)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"Training samples: {len(X_train)}, Testing samples: {len(X_test)}")
    
    # Vectorizer (TF-IDF with sublinear tf and ngram_range 1-2)
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.9,
        sublinear_tf=True
    )
    
    print("Fitting vectorizer...")
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    print(f"Vocabulary size: {len(vectorizer.vocabulary_)} features")
    
    # Models to evaluate (Slide 8 & 10)
    models = {
        "Naive Bayes (MultinomialNB)": MultinomialNB(alpha=1.0), # Laplace smoothing alpha=1
        "Naive Bayes (BernoulliNB)": BernoulliNB(alpha=1.0),
        "Decision Tree": DecisionTreeClassifier(max_depth=20, random_state=42),
        "KNN": KNeighborsClassifier(n_neighbors=5, metric='cosine'),
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42)
    }
    
    benchmark_results = {
        "dataset_info": {
            "total_samples": int(len(df)),
            "train_samples": int(len(X_train)),
            "test_samples": int(len(X_test)),
            "categories": CATEGORIES,
            "category_distribution": df['category'].value_counts().to_dict(),
            "sources": df['source'].value_counts().to_dict()
        },
        "models": {},
        "learning_curve": {
            "sample_sizes": [],
            "nb_accuracies": []
        }
    }
    
    trained_models = {}
    
    for name, model in models.items():
        print(f"\n--- Training {name} ---")
        t0 = time.time()
        model.fit(X_train_vec, y_train)
        train_time = time.time() - t0
        
        # Test inference time (batch and per-sample ms)
        t_inf_start = time.time()
        y_pred = model.predict(X_test_vec)
        inf_total = time.time() - t_inf_start
        latency_ms = (inf_total / len(X_test)) * 1000
        
        acc = accuracy_score(y_test, y_pred)
        
        # Top-3 Accuracy if predict_proba supported
        if hasattr(model, "predict_proba"):
            top3_acc = top_k_accuracy(model, X_test_vec, y_test, k=3)
        else:
            top3_acc = acc
            
        p_macro, r_macro, f1_macro, _ = precision_recall_fscore_support(y_test, y_pred, average='macro', zero_division=0)
        p_weight, r_weight, f1_weight, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted', zero_division=0)
        
        # Per-class metrics
        p_class, r_class, f1_class, support_class = precision_recall_fscore_support(
            y_test, y_pred, labels=CATEGORIES, zero_division=0
        )
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred, labels=CATEGORIES)
        
        per_class_results = {}
        for idx, cat in enumerate(CATEGORIES):
            per_class_results[cat] = {
                "precision": round(float(p_class[idx]) * 100, 2),
                "recall": round(float(r_class[idx]) * 100, 2),
                "f1_score": round(float(f1_class[idx]) * 100, 2),
                "support": int(support_class[idx])
            }
            
        benchmark_results["models"][name] = {
            "accuracy": round(float(acc) * 100, 2),
            "top3_accuracy": round(float(top3_acc) * 100, 2),
            "macro_precision": round(float(p_macro) * 100, 2),
            "macro_recall": round(float(r_macro) * 100, 2),
            "macro_f1": round(float(f1_macro) * 100, 2),
            "weighted_f1": round(float(f1_weight) * 100, 2),
            "latency_ms": round(float(latency_ms), 3),
            "train_time_sec": round(float(train_time), 3),
            "per_class": per_class_results,
            "confusion_matrix": cm.tolist()
        }
        
        trained_models[name] = model
        print(f"Accuracy: {acc*100:.2f}% | Top-3 Accuracy: {top3_acc*100:.2f}% | Inference latency: {latency_ms:.3f} ms")

    # Learning curve for Naive Bayes (Slide 10)
    print("\nCalculating Learning Curve for Naive Bayes...")
    sample_sizes = [500, 1000, 2000, 5000, 10000, len(X_train)]
    nb_learning_accs = []
    
    for size in sample_sizes:
        if size > len(X_train):
            continue
        X_sub = X_train[:size]
        y_sub = y_train[:size]
        vec_sub = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_df=0.9, sublinear_tf=True)
        X_sub_vec = vec_sub.fit_transform(X_sub)
        X_test_sub = vec_sub.transform(X_test)
        
        nb_model = MultinomialNB(alpha=1.0)
        nb_model.fit(X_sub_vec, y_sub)
        sub_acc = accuracy_score(y_test, nb_model.predict(X_test_sub))
        nb_learning_accs.append(round(float(sub_acc) * 100, 2))
        print(f"  Train Size: {size} -> Accuracy: {sub_acc*100:.2f}%")
        
    benchmark_results["learning_curve"]["sample_sizes"] = sample_sizes
    benchmark_results["learning_curve"]["nb_accuracies"] = nb_learning_accs

    # Save primary model and vectorizer
    primary_nb = trained_models["Naive Bayes (MultinomialNB)"]
    joblib.dump(primary_nb, os.path.join(MODEL_DIR, "naive_bayes_model.joblib"))
    joblib.dump(vectorizer, os.path.join(MODEL_DIR, "vectorizer.joblib"))
    
    # Save benchmark results
    with open(os.path.join(MODEL_DIR, "benchmark_results.json"), "w", encoding="utf-8") as f:
        json.dump(benchmark_results, f, ensure_ascii=False, indent=2)
        
    print(f"\nAll models trained and saved to {MODEL_DIR} successfully!")
    return benchmark_results

if __name__ == '__main__':
    train_and_evaluate()
