import pandas as pd
from pathlib import Path
from sklearn.ensemble import IsolationForest


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

GOLD_DIR = PROJECT_ROOT / "data" / "gold"


# --------------------------------------------------
# 2. Read tower health data
# --------------------------------------------------

print("Reading Gold layer...")

df = pd.read_parquet(
    GOLD_DIR / "tower_health.parquet"
)

print("Towers loaded:", len(df))


# --------------------------------------------------
# 3. Select network features
# --------------------------------------------------

features = [
    "avg_latency_ms",
    "avg_packet_loss_pct",
    "avg_cpu_utilization_pct",
    "avg_call_drop_rate",
    "avg_connection_failure_rate",
    "avg_signal_strength_dbm",
    "avg_active_users"
]

X = df[features].copy()


# --------------------------------------------------
# 4. Create Isolation Forest model
# --------------------------------------------------

print("\nRunning anomaly detection...")

model = IsolationForest(
    contamination=0.05,
    random_state=42
)


# --------------------------------------------------
# 5. Detect anomalies
# --------------------------------------------------

df["anomaly_prediction"] = model.fit_predict(X)

df["anomaly_score"] = model.decision_function(X)


# --------------------------------------------------
# 6. Convert prediction into readable labels
# --------------------------------------------------

df["anomaly_status"] = df["anomaly_prediction"].apply(
    lambda x: "Anomaly" if x == -1 else "Normal"
)


# --------------------------------------------------
# 7. Save anomaly results
# --------------------------------------------------

output_file = GOLD_DIR / "tower_anomaly_detection.csv"

df.to_csv(
    output_file,
    index=False
)


# Also save as Parquet

df.to_parquet(
    GOLD_DIR / "tower_anomaly_detection.parquet",
    index=False
)


# --------------------------------------------------
# 8. Display results
# --------------------------------------------------

print("\n==========================================")
print("ANOMALY DETECTION COMPLETED")
print("==========================================")

print("\nAnomaly counts:")

print(
    df["anomaly_status"].value_counts()
)


print("\nDetected anomalies:")

print(
    df[
        df["anomaly_status"] == "Anomaly"
    ][
        [
            "tower_id",
            "region",
            "technology",
            "tower_health_score",
            "tower_status",
            "anomaly_score",
            "problem_indicators"
        ]
    ]
    .sort_values("anomaly_score")
    .head(20)
)


print("\nResults saved to:")

print(output_file)
