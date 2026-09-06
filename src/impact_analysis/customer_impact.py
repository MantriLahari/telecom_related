import pandas as pd
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

GOLD_DIR = PROJECT_ROOT / "data" / "gold"
RAW_DIR = PROJECT_ROOT / "data" / "raw"


# ============================================================
# LOAD TOWER FAILURE PREDICTIONS
# ============================================================

print("Loading tower predictions...")

predictions_file = GOLD_DIR / "tower_failure_predictions.csv"

predictions = pd.read_csv(predictions_file)

print(f"Tower prediction records: {len(predictions)}")


# ============================================================
# LOAD TOWER HEALTH DATA
# ============================================================

print("\nLoading tower health data...")

health_file = GOLD_DIR / "tower_health.csv"

tower_health = pd.read_csv(health_file)

print(f"Tower health records: {len(tower_health)}")


# ============================================================
# LOAD CUSTOMER DATA
# ============================================================

print("\nLoading customers...")

customers_file = RAW_DIR / "customers.csv"

customers = pd.read_csv(customers_file)

print(f"Customer records: {len(customers)}")


# ============================================================
# SELECT TOWER HEALTH COLUMNS
# ============================================================

tower_health_data = tower_health[
    [
        "tower_id",
        "region",
        "technology",
        "tower_health_score",
        "tower_status",
        "problem_indicators"
    ]
].copy()


# ============================================================
# SELECT PREDICTION COLUMNS
# ============================================================

prediction_data = predictions[
    [
        "tower_id",
        "failure_probability",
        "risk_category",
        "recommended_action"
    ]
].copy()


# ============================================================
# MERGE TOWER HEALTH + PREDICTIONS
# ============================================================

tower_data = pd.merge(
    tower_health_data,
    prediction_data,
    on="tower_id",
    how="inner"
)

print("\nCombined tower records:", len(tower_data))


# ============================================================
# MERGE CUSTOMERS WITH TOWER DATA
# ============================================================

customer_impact = pd.merge(
    customers,
    tower_data,
    on="tower_id",
    how="left",
    suffixes=("_customer", "_tower")
)


# ============================================================
# FIX REGION
# ============================================================

# Customer data already contains region.
# We use the tower region as the authoritative network region.

if "region_tower" in customer_impact.columns:
    customer_impact["network_region"] = customer_impact["region_tower"]
else:
    customer_impact["network_region"] = customer_impact["region"]


# ============================================================
# IDENTIFY POTENTIALLY AFFECTED CUSTOMERS
# ============================================================

customer_impact["potentially_affected"] = (
    customer_impact["risk_category"].isin(
        ["HIGH", "CRITICAL"]
    )
)


# ============================================================
# CALCULATE REVENUE AT RISK
# ============================================================

customer_impact["revenue_at_risk"] = (
    customer_impact["monthly_revenue"]
    * customer_impact["potentially_affected"]
)


# ============================================================
# IDENTIFY HIGH-VALUE CUSTOMERS
# ============================================================

customer_impact["high_value_customer"] = (
    customer_impact["plan"].isin(
        ["Premium", "Unlimited"]
    )
)


customer_impact["high_value_at_risk"] = (
    customer_impact["high_value_customer"]
    & customer_impact["potentially_affected"]
)


# ============================================================
# CUSTOMER IMPACT SUMMARY
# ============================================================

total_customers = len(customer_impact)

affected_customers = int(
    customer_impact["potentially_affected"].sum()
)

revenue_at_risk = customer_impact[
    "revenue_at_risk"
].sum()

high_value_at_risk = int(
    customer_impact["high_value_at_risk"].sum()
)


print("\n==============================================")
print("CUSTOMER IMPACT SUMMARY")
print("==============================================")

print(f"Total customers: {total_customers:,}")

print(
    f"Potentially affected customers: "
    f"{affected_customers:,}"
)

print(
    f"Monthly revenue at risk: "
    f"${revenue_at_risk:,.2f}"
)

print(
    f"High-value customers at risk: "
    f"{high_value_at_risk:,}"
)


# ============================================================
# TOWER-LEVEL CUSTOMER IMPACT
# ============================================================

tower_customer_impact = (
    customer_impact
    .groupby(
        [
            "tower_id",
            "network_region",
            "technology",
            "tower_health_score",
            "tower_status",
            "risk_category",
            "failure_probability",
            "recommended_action"
        ],
        as_index=False
    )
    .agg(
        total_customers=("customer_id", "count"),
        affected_customers=("potentially_affected", "sum"),
        monthly_revenue=("monthly_revenue", "sum"),
        revenue_at_risk=("revenue_at_risk", "sum")
    )
)


# ============================================================
# REGIONAL CUSTOMER IMPACT
# ============================================================

regional_customer_impact = (
    customer_impact
    .groupby(
        "network_region",
        as_index=False
    )
    .agg(
        total_customers=("customer_id", "count"),
        affected_customers=("potentially_affected", "sum"),
        monthly_revenue=("monthly_revenue", "sum"),
        revenue_at_risk=("revenue_at_risk", "sum")
    )
)


# ============================================================
# SAVE CUSTOMER-LEVEL OUTPUT
# ============================================================

customer_output = GOLD_DIR / "customer_impact.csv"

customer_impact.to_csv(
    customer_output,
    index=False
)


# ============================================================
# SAVE TOWER-LEVEL OUTPUT
# ============================================================

tower_output = GOLD_DIR / "tower_customer_impact.csv"

tower_customer_impact.to_csv(
    tower_output,
    index=False
)


# ============================================================
# SAVE REGIONAL OUTPUT
# ============================================================

regional_output = GOLD_DIR / "regional_customer_impact.csv"

regional_customer_impact.to_csv(
    regional_output,
    index=False
)


# ============================================================
# FINAL RESULT
# ============================================================

print("\n==============================================")
print("FILES CREATED SUCCESSFULLY")
print("==============================================")

print(
    f"Customer impact: "
    f"{customer_output}"
)

print(
    f"Tower impact: "
    f"{tower_output}"
)

print(
    f"Regional impact: "
    f"{regional_output}"
)

print("\nCustomer impact analysis completed successfully!")

