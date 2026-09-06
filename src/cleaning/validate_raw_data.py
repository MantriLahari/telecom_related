import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# 1. FIND PROJECT DIRECTORY
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


# ---------------------------------------------------------
# 2. FUNCTION TO CHECK A DATASET
# ---------------------------------------------------------

def validate_dataset(file_name):

    file_path = RAW_DATA_DIR / file_name

    print("\n" + "=" * 70)
    print(f"VALIDATING: {file_name}")
    print("=" * 70)

    # Check whether file exists
    if not file_path.exists():
        print("ERROR: File does not exist!")
        return

    # Read CSV
    df = pd.read_csv(file_path)

    # -----------------------------------------------------
    # BASIC INFORMATION
    # -----------------------------------------------------

    print("\nRows:", len(df))
    print("Columns:", len(df.columns))

    print("\nColumn names:")
    print(list(df.columns))

    # -----------------------------------------------------
    # MISSING VALUES
    # -----------------------------------------------------

    print("\nMissing values:")

    missing = df.isnull().sum()

    print(missing[missing > 0])

    if missing.sum() == 0:
        print("No missing values found.")

    # -----------------------------------------------------
    # DUPLICATES
    # -----------------------------------------------------

    duplicates = df.duplicated().sum()

    print("\nDuplicate rows:", duplicates)

    # -----------------------------------------------------
    # DATA TYPES
    # -----------------------------------------------------

    print("\nData types:")

    print(df.dtypes)

    # -----------------------------------------------------
    # FIRST FIVE RECORDS
    # -----------------------------------------------------

    print("\nFirst 5 records:")

    print(df.head())

    # -----------------------------------------------------
    # NUMERIC SUMMARY
    # -----------------------------------------------------

    print("\nNumerical statistics:")

    print(df.describe())


# ---------------------------------------------------------
# 3. VALIDATE ALL DATASETS
# ---------------------------------------------------------

files = [
    "towers.csv",
    "network_telemetry.csv",
    "tower_faults.csv",
    "customers.csv",
    "network_events.csv"
]


for file in files:

    validate_dataset(file)


# ---------------------------------------------------------
# 4. SPECIAL TELEMETRY CHECKS
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("TELEMETRY QUALITY CHECKS")
print("=" * 70)

telemetry_file = RAW_DATA_DIR / "network_telemetry.csv"

telemetry = pd.read_csv(telemetry_file)


# Check latency
invalid_latency = (
    telemetry["latency_ms"] < 0
).sum()

print(
    "\nNegative latency records:",
    invalid_latency
)


# Check packet loss
invalid_packet_loss = (
    (telemetry["packet_loss_pct"] < 0) |
    (telemetry["packet_loss_pct"] > 100)
).sum()

print(
    "Invalid packet loss records:",
    invalid_packet_loss
)


# Check CPU
invalid_cpu = (
    (telemetry["cpu_utilization_pct"] < 0) |
    (telemetry["cpu_utilization_pct"] > 100)
).sum()

print(
    "Invalid CPU records:",
    invalid_cpu
)


# Check call drop rate
invalid_call_drop = (
    (telemetry["call_drop_rate"] < 0) |
    (telemetry["call_drop_rate"] > 100)
).sum()

print(
    "Invalid call-drop records:",
    invalid_call_drop
)


# ---------------------------------------------------------
# 5. TOWER COUNT
# ---------------------------------------------------------

unique_towers = telemetry["tower_id"].nunique()

print(
    "\nUnique towers in telemetry:",
    unique_towers
)


# ---------------------------------------------------------
# 6. DATE RANGE
# ---------------------------------------------------------

telemetry["timestamp"] = pd.to_datetime(
    telemetry["timestamp"]
)

print(
    "\nTelemetry start:",
    telemetry["timestamp"].min()
)

print(
    "Telemetry end:",
    telemetry["timestamp"].max()
)


# ---------------------------------------------------------
# 7. FINAL RESULT
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("DATA VALIDATION COMPLETED")
print("=" * 70)
