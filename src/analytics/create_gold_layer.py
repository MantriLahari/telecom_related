import pandas as pd
import numpy as np
from pathlib import Path


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SILVER_DIR = PROJECT_ROOT / "data" / "processed"
GOLD_DIR = PROJECT_ROOT / "data" / "gold"

GOLD_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. Read Silver data
# --------------------------------------------------

print("Reading Silver telemetry data...")

telemetry = pd.read_parquet(
    SILVER_DIR / "network_telemetry.parquet"
)

towers = pd.read_parquet(
    SILVER_DIR / "towers.parquet"
)

print("Telemetry records:", len(telemetry))
print("Towers:", len(towers))


# --------------------------------------------------
# 3. Aggregate telemetry for each tower
# --------------------------------------------------

print("\nCalculating tower metrics...")


tower_metrics = telemetry.groupby("tower_id").agg(

    avg_latency_ms=("latency_ms", "mean"),

    avg_packet_loss_pct=("packet_loss_pct", "mean"),

    avg_download_mbps=("download_mbps", "mean"),

    avg_upload_mbps=("upload_mbps", "mean"),

    avg_signal_strength_dbm=("signal_strength_dbm", "mean"),

    avg_cpu_utilization_pct=("cpu_utilization_pct", "mean"),

    avg_memory_utilization_pct=("memory_utilization_pct", "mean"),

    avg_call_drop_rate=("call_drop_rate", "mean"),

    avg_connection_failure_rate=("connection_failure_rate", "mean"),

    avg_active_users=("active_users", "mean")

).reset_index()


# --------------------------------------------------
# 4. Join tower information
# --------------------------------------------------

tower_metrics = tower_metrics.merge(
    towers[
        [
            "tower_id",
            "region",
            "technology",
            "latitude",
            "longitude",
            "installation_year"
        ]
    ],
    on="tower_id",
    how="left"
)


# --------------------------------------------------
# 5. Calculate health components
# --------------------------------------------------

print("Calculating health score...")


# Latency score
latency_score = 100 - (
    tower_metrics["avg_latency_ms"] / 200 * 100
)

latency_score = latency_score.clip(0, 100)


# Packet loss score
packet_loss_score = 100 - (
    tower_metrics["avg_packet_loss_pct"] / 10 * 100
)

packet_loss_score = packet_loss_score.clip(0, 100)


# CPU score
cpu_score = 100 - tower_metrics["avg_cpu_utilization_pct"]

cpu_score = cpu_score.clip(0, 100)


# Call drop score
call_drop_score = 100 - (
    tower_metrics["avg_call_drop_rate"] / 10 * 100
)

call_drop_score = call_drop_score.clip(0, 100)


# Connection failure score
connection_score = 100 - (
    tower_metrics["avg_connection_failure_rate"] / 10 * 100
)

connection_score = connection_score.clip(0, 100)


# Signal score
#
# -70 dBm is considered stronger than -110 dBm.
#

signal_score = (
    (tower_metrics["avg_signal_strength_dbm"] + 110)
    / 40
    * 100
)

signal_score = signal_score.clip(0, 100)


# --------------------------------------------------
# 6. Calculate final Tower Health Score
# --------------------------------------------------

tower_metrics["tower_health_score"] = (

    latency_score * 0.20 +

    packet_loss_score * 0.20 +

    cpu_score * 0.15 +

    call_drop_score * 0.15 +

    connection_score * 0.10 +

    signal_score * 0.20

)


tower_metrics["tower_health_score"] = (
    tower_metrics["tower_health_score"]
    .round(2)
)


# --------------------------------------------------
# 7. Assign tower status
# --------------------------------------------------

def get_status(score):

    if score >= 80:
        return "Healthy"

    elif score >= 60:
        return "Warning"

    elif score >= 40:
        return "Critical"

    else:
        return "Severe"


tower_metrics["tower_status"] = (
    tower_metrics["tower_health_score"]
    .apply(get_status)
)


# --------------------------------------------------
# 8. Identify major problem indicators
# --------------------------------------------------

def identify_issue(row):

    issues = []

    if row["avg_latency_ms"] > 100:
        issues.append("High Latency")

    if row["avg_packet_loss_pct"] > 5:
        issues.append("Packet Loss")

    if row["avg_cpu_utilization_pct"] > 80:
        issues.append("High CPU")

    if row["avg_call_drop_rate"] > 5:
        issues.append("Call Drops")

    if row["avg_connection_failure_rate"] > 5:
        issues.append("Connection Failures")

    if row["avg_signal_strength_dbm"] < -100:
        issues.append("Weak Signal")

    if len(issues) == 0:
        return "No Major Issue"

    return ", ".join(issues)


tower_metrics["problem_indicators"] = tower_metrics.apply(
    identify_issue,
    axis=1
)


# --------------------------------------------------
# 9. Save Tower Gold table
# --------------------------------------------------

tower_metrics.to_parquet(
    GOLD_DIR / "tower_health.parquet",
    index=False
)

tower_metrics.to_csv(
    GOLD_DIR / "tower_health.csv",
    index=False
)


# --------------------------------------------------
# 10. Create Region Summary
# --------------------------------------------------

print("\nCreating regional summary...")


region_summary = tower_metrics.groupby("region").agg(

    total_towers=("tower_id", "count"),

    average_health_score=("tower_health_score", "mean"),

    average_latency_ms=("avg_latency_ms", "mean"),

    average_packet_loss_pct=("avg_packet_loss_pct", "mean"),

    average_call_drop_rate=("avg_call_drop_rate", "mean"),

    average_connection_failure_rate=(
        "avg_connection_failure_rate",
        "mean"
    ),

    average_cpu_utilization=(
        "avg_cpu_utilization_pct",
        "mean"
    ),

    average_active_users=("avg_active_users", "mean")

).reset_index()


region_summary["average_health_score"] = (
    region_summary["average_health_score"].round(2)
)


# --------------------------------------------------
# 11. Save Region Gold table
# --------------------------------------------------

region_summary.to_parquet(
    GOLD_DIR / "region_network_summary.parquet",
    index=False
)

region_summary.to_csv(
    GOLD_DIR / "region_network_summary.csv",
    index=False
)


# --------------------------------------------------
# 12. Print results
# --------------------------------------------------

print("\n==========================================")
print("GOLD LAYER CREATED SUCCESSFULLY")
print("==========================================")

print("\nTower Health Preview:")
print(
    tower_metrics[
        [
            "tower_id",
            "region",
            "technology",
            "tower_health_score",
            "tower_status",
            "problem_indicators"
        ]
    ].head(10)
)

print("\nRegional Summary:")
print(region_summary)

print("\nGold files saved to:")
print(GOLD_DIR)