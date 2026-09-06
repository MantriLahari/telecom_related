import pandas as pd
from pathlib import Path
from datetime import datetime


# =========================================================
# 1. PROJECT DIRECTORIES
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

BRONZE_DATA_DIR = PROJECT_ROOT / "data" / "bronze"


# Create Bronze directory
BRONZE_DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# 2. INGESTION FUNCTION
# =========================================================

def ingest_file(file_path):

    print("\n" + "-" * 60)

    print("Processing:", file_path.name)

    # -----------------------------------------------------
    # Read raw CSV
    # -----------------------------------------------------

    df = pd.read_csv(file_path)

    print(
        "Records read:",
        f"{len(df):,}"
    )

    # -----------------------------------------------------
    # Add ingestion metadata
    # -----------------------------------------------------

    df["ingestion_timestamp"] = datetime.now()

    df["source_file"] = file_path.name

    # -----------------------------------------------------
    # Create Bronze filename
    # -----------------------------------------------------

    bronze_file_name = (
        file_path.stem + ".parquet"
    )

    bronze_file_path = (
        BRONZE_DATA_DIR /
        bronze_file_name
    )

    # -----------------------------------------------------
    # Save as Parquet
    # -----------------------------------------------------

    df.to_parquet(
        bronze_file_path,
        index=False
    )

    print(
        "Bronze file created:",
        bronze_file_path.name
    )

    print(
        "Records written:",
        f"{len(df):,}"
    )


# =========================================================
# 3. FIND RAW FILES
# =========================================================

print("=" * 60)

print("TELECOM DATA INGESTION PIPELINE")

print("=" * 60)

print("\nRaw data directory:")

print(RAW_DATA_DIR)


raw_files = list(
    RAW_DATA_DIR.glob("*.csv")
)


print(
    f"\nCSV files found: {len(raw_files)}"
)


# =========================================================
# 4. INGEST EACH FILE
# =========================================================

for file_path in raw_files:

    ingest_file(file_path)


# =========================================================
# 5. FINAL SUMMARY
# =========================================================

print("\n" + "=" * 60)

print("BRONZE INGESTION COMPLETED")

print("=" * 60)

bronze_files = list(
    BRONZE_DATA_DIR.glob("*.parquet")
)

print(
    f"\nBronze files created: {len(bronze_files)}"
)

for file in bronze_files:

    print(
        " -",
        file.name
    )

print("\nPipeline completed successfully.")
