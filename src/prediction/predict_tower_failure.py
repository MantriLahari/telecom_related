import pandas as pd
import numpy as np
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SILVER_DIR = PROJECT_ROOT / "data" / "processed"
GOLD_DIR = PROJECT_ROOT / "data" / "gold"

print("Project root:", PROJECT_ROOT)


# ============================================================
# 2. LOAD TELEMETRY
# ============================================================

print("\nLoading telemetry...")

telemetry = pd.read_parquet(
    SILVER_DIR / "network_telemetry.parquet"
)

print("Telemetry records:", len(telemetry))


# ============================================================
# 3. LOAD HISTORICAL FAULTS
# ============================================================

print("\nLoading tower faults...")

faults = pd.read_parquet(
    SILVER_DIR / "tower_faults.parquet"
)

print("Fault records:", len(faults))


# ============================================================
# 4. CREATE TOWER-LEVEL TELEMETRY FEATURES
# ============================================================

print("\nCreating tower features...")

tower_features = telemetry.groupby("tower_id").agg(

    avg_latency_ms=("latency_ms", "mean"),

    avg_packet_loss_pct=("packet_loss_pct", "mean"),

    avg_download_mbps=("download_mbps", "mean"),

    avg_upload_mbps=("upload_mbps", "mean"),

    avg_signal_strength_dbm=("signal_strength_dbm", "mean"),

    avg_cpu_utilization_pct=("cpu_utilization_pct", "mean"),

    avg_memory_utilization_pct=("memory_utilization_pct", "mean"),

    avg_call_drop_rate=("call_drop_rate", "mean"),

    avg_connection_failure_rate=(
        "connection_failure_rate",
        "mean"
    ),

    avg_active_users=("active_users", "mean")

).reset_index()


# ============================================================
# 5. CREATE FAULT LABEL
# ============================================================

print("\nCreating failure labels...")

fault_counts = (
    faults
    .groupby("tower_id")
    .size()
    .reset_index(name="fault_count")
)


# Add fault count to tower features

tower_features = tower_features.merge(
    fault_counts,
    on="tower_id",
    how="left"
)


# Towers without faults get 0

tower_features["fault_count"] = (
    tower_features["fault_count"]
    .fillna(0)
)


# ============================================================
# 6. CREATE BINARY TARGET
# ============================================================

# 1 = tower has experienced a fault
# 0 = tower has not experienced a fault

tower_features["failure"] = (
    tower_features["fault_count"] > 0
).astype(int)


print("\nFailure distribution:")

print(
    tower_features["failure"].value_counts()
)


# ============================================================
# 7. SELECT ML FEATURES
# ============================================================

features = [

    "avg_latency_ms",

    "avg_packet_loss_pct",

    "avg_download_mbps",

    "avg_upload_mbps",

    "avg_signal_strength_dbm",

    "avg_cpu_utilization_pct",

    "avg_memory_utilization_pct",

    "avg_call_drop_rate",

    "avg_connection_failure_rate",

    "avg_active_users"

]


X = tower_features[features]

y = tower_features["failure"]


# ============================================================
# 8. TRAIN / TEST SPLIT
# ============================================================

print("\nSplitting data...")

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y

)


print("Training records:", len(X_train))

print("Testing records:", len(X_test))


# ============================================================
# 9. CREATE RANDOM FOREST MODEL
# ============================================================

print("\nTraining Random Forest model...")

model = RandomForestClassifier(

    n_estimators=200,

    max_depth=8,

    random_state=42,

    class_weight="balanced"

)


# ============================================================
# 10. TRAIN MODEL
# ============================================================

model.fit(
    X_train,
    y_train
)


print("Model training completed.")


# ============================================================
# 11. TEST MODEL
# ============================================================

y_pred = model.predict(X_test)


accuracy = accuracy_score(
    y_test,
    y_pred
)


print("\n===================================")
print("MODEL PERFORMANCE")
print("===================================")

print(
    "Accuracy:",
    round(accuracy, 4)
)


print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)


# ============================================================
# 12. PREDICT FAILURE PROBABILITY
# ============================================================

tower_features["failure_probability"] = (

    model.predict_proba(X)[:, 1]

)


# Convert to percentage

tower_features["failure_probability"] = (

    tower_features["failure_probability"] * 100

).round(2)


# ============================================================
# 13. CREATE RISK CATEGORY
# ============================================================

def risk_category(probability):

    if probability >= 75:
        return "CRITICAL"

    elif probability >= 50:
        return "HIGH"

    elif probability >= 25:
        return "MEDIUM"

    else:
        return "LOW"


tower_features["risk_category"] = (

    tower_features["failure_probability"]
    .apply(risk_category)

)


# ============================================================
# 14. RECOMMENDED ACTION
# ============================================================

def recommended_action(risk):

    if risk == "CRITICAL":
        return "Immediate technician inspection"

    elif risk == "HIGH":
        return "Schedule preventive maintenance"

    elif risk == "MEDIUM":
        return "Increase monitoring frequency"

    else:
        return "Normal monitoring"


tower_features["recommended_action"] = (

    tower_features["risk_category"]
    .apply(recommended_action)

)


# ============================================================
# 15. SAVE RESULTS
# ============================================================

output_file = (

    GOLD_DIR /
    "tower_failure_predictions.csv"

)


tower_features.to_csv(

    output_file,

    index=False

)


tower_features.to_parquet(

    GOLD_DIR /
    "tower_failure_predictions.parquet",

    index=False

)


# ============================================================
# 16. DISPLAY HIGH-RISK TOWERS
# ============================================================

print("\n===================================")
print("TOP HIGH-RISK TOWERS")
print("===================================")


high_risk = (

    tower_features
    .sort_values(
        "failure_probability",
        ascending=False
    )
    .head(20)

)


print(

    high_risk[
        [
            "tower_id",
            "failure_probability",
            "risk_category",
            "fault_count",
            "recommended_action"
        ]
    ]

)


# ============================================================
# 17. RISK SUMMARY
# ============================================================

print("\n===================================")
print("RISK SUMMARY")
print("===================================")

print(

    tower_features[
        "risk_category"
    ].value_counts()

)


print("\nPrediction results saved to:")

print(output_file)

print("\nDONE!")
