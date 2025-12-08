import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from joblib import dump

print("=" * 60)
print("🛡️  KEVLAR - PHISHGUARD MODEL TRAINING")
print("=" * 60)

# ================================
# 1. LOAD DATASET
# ================================

DATASET_PATH = "urlset.csv"
print("📂 Loading dataset from:", DATASET_PATH)

df = pd.read_csv(
    DATASET_PATH,
    on_bad_lines="skip",
    encoding="latin-1",
    low_memory=False
)

print("✅ Dataset loaded successfully")
print("Initial shape:", df.shape)

# ================================
# 2. CLEAN DATA
# ================================

print("🧹 Cleaning data...")

# Convert all columns except domain + label to numeric
for col in df.columns:
    if col not in ["domain", "label"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove rows where label is missing
df = df.dropna(subset=["label"])

# Fill missing numeric values with 0
df = df.fillna(0)

print("✅ Data cleaned")
print("Cleaned shape:", df.shape)

# ================================
# 3. SPLIT FEATURES & LABELS
# ================================

y = df["label"]
X = df.drop(columns=["label", "domain"], errors="ignore")

print("✅ Feature matrix ready")
print("Final feature count:", X.shape[1])

# ================================
# 4. TRAIN / TEST SPLIT
# ================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("✅ Data split completed")
print("Train size:", X_train.shape)
print("Test size :", X_test.shape)

# ================================
# 5. MODEL TRAINING
# ================================

print("🤖 Training Random Forest model...")

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=None,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

print("✅ Model training completed")

# ================================
# 6. MODEL EVALUATION
# ================================

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("\n📊 Model Evaluation")
print("-" * 40)
print(f"✅ Accuracy: {accuracy * 100:.2f}%\n")
print("📄 Classification Report:\n")
print(classification_report(y_test, y_pred))

# ================================
# 7. SAVE MODEL TO KEVLAR BACKEND
# ================================

OUTPUT_PATH = "../backend/model.pkl"

dump(model, OUTPUT_PATH)

print("✅ Model successfully saved to:")
print("   ", os.path.abspath(OUTPUT_PATH))

print("=" * 60)
print("🚀 KEVLAR TRAINING PIPELINE COMPLETED")
print("=" * 60)
