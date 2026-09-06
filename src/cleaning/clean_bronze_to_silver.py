import pandas as pd
from pathlib import Path


# --------------------------------------------------
# 1. Find project folder
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

BRONZE_DIR = PROJECT_ROOT / "data" / "bronze"
SILVER_DIR = PROJECT_ROOT / "data" / "processed"

SILVER_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. Function to clean a dataframe
# --------------------------------------------------

def clean_dataframe(df):

    # Remove duplicate records
    df = df.drop_duplicates()

    # Remove completely empty rows
    df = df.dropna(how="all")

    return df


# --------------------------------------------------
# 3. Clean Towers
# --------------------------------------------------

print("\nCleaning towers...")

towers = pd.read_parquet(BRONZE_DIR / "towers.parquet")

towers = clean_dataframe(towers)

# Remove invalid installation years
towers = towers[
    (towers["installation_year"] >= 2000) &
    (towers["installation_year"] <= 2026)
]

# Standardize text columns
towers["region"] = towers["region"].str.strip().str.title()
towers["technology"] = towers["technology"].str.strip().str.upper()

towers.to_parquet(
    SILVER_DIR / "towers.parquet",
    index=False
)

print("Towers cleaned:", len(towers))


# --------------------------------------------------
# 4. Clean Network Telemetry
# --------------------------------------------------

print("\nCleaning network telemetry...")

telemetry = pd.read_parquet(
    BRONZE_DIR / "network_telemetry.parquet"
)

telemetry = clean_dataframe(telemetry)

# Convert timestamp
telemetry["timestamp"] = pd.to_datetime(
    telemetry["timestamp"],
    errors="coerce"
)

# Remove rows where timestamp is invalid
telemetry = telemetry.dropna(subset=["timestamp"])

# Remove invalid network measurements
telemetry = telemetry[
    (telemetry["latency_ms"] >= 0) &
    (telemetry["packet_loss_pct"].between(0, 100)) &
    (telemetry["cpu_utilization_pct"].between(0, 100)) &
    (telemetry["memory_utilization_pct"].between(0, 100)) &
    (telemetry["call_drop_rate"].between(0, 100)) &
    (telemetry["connection_failure_rate"].between(0, 100))
]

# Make tower IDs consistent
telemetry["tower_id"] = telemetry["tower_id"].str.strip().str.upper()

telemetry.to_parquet(
    SILVER_DIR / "network_telemetry.parquet",
    index=False
)

print("Telemetry cleaned:", len(telemetry))


# --------------------------------------------------
# 5. Clean Tower Faults
# --------------------------------------------------

print("\nCleaning tower faults...")

faults = pd.read_parquet(
    BRONZE_DIR / "tower_faults.parquet"
)

faults = clean_dataframe(faults)

faults["timestamp"] = pd.to_datetime(
    faults["timestamp"],
    errors="coerce"
)

faults = faults.dropna(subset=["timestamp"])

faults["tower_id"] = faults["tower_id"].str.strip().str.upper()

faults["fault_type"] = faults["fault_type"].str.strip().str.title()

faults["severity"] = faults["severity"].str.strip().str.title()

faults["resolved"] = faults["resolved"].astype(bool)

faults.to_parquet(
    SILVER_DIR / "tower_faults.parquet",
    index=False
)

print("Faults cleaned:", len(faults))


# --------------------------------------------------
# 6. Clean Customers
# --------------------------------------------------

print("\nCleaning customers...")

customers = pd.read_parquet(
    BRONZE_DIR / "customers.parquet"
)

customers = clean_dataframe(customers)

customers["tower_id"] = customers["tower_id"].str.strip().str.upper()
customers["region"] = customers["region"].str.strip().str.title()
customers["plan"] = customers["plan"].str.strip().str.title()

# Revenue and usage cannot be negative
customers = customers[
    (customers["monthly_revenue"] >= 0) &
    (customers["data_usage_gb"] >= 0) &
    (customers["complaint_count"] >= 0)
]

customers.to_parquet(
    SILVER_DIR / "customers.parquet",
    index=False
)

print("Customers cleaned:", len(customers))


# --------------------------------------------------
# 7. Clean Network Events
# --------------------------------------------------

print("\nCleaning network events...")

events = pd.read_parquet(
    BRONZE_DIR / "network_events.parquet"
)

events = clean_dataframe(events)

events["timestamp"] = pd.to_datetime(
    events["timestamp"],
    errors="coerce"
)

events = events.dropna(subset=["timestamp"])

events["tower_id"] = events["tower_id"].str.strip().str.upper()

events["event_type"] = events["event_type"].str.strip().str.title()

events["severity"] = events["severity"].str.strip().str.title()

events.to_parquet(
    SILVER_DIR / "network_events.parquet",
    index=False
)

print("Network events cleaned:", len(events))


# --------------------------------------------------
# 8. Finished
# --------------------------------------------------

print("\n====================================")
print("SILVER LAYER CREATED SUCCESSFULLY")
print("====================================")

print("\nFiles saved in:")
print(SILVER_DIR)