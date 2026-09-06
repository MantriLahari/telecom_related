# import pandas as pd
# import numpy as np
# from faker import Faker
# from pathlib import Path
# from datetime import datetime, timedelta
# import random

# # ---------------------------------------------------------
# # 1. BASIC CONFIGURATION
# # ---------------------------------------------------------

# fake = Faker()
# random.seed(42)
# np.random.seed(42)

# # Project root directory
# PROJECT_ROOT = Path(__file__).resolve().parents[2]

# # Output directory
# RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

# # Create directory if it doesn't exist
# RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

# print("Project root:", PROJECT_ROOT)
# print("Raw data directory:", RAW_DATA_DIR)


# # ---------------------------------------------------------
# # 2. GENERATE TOWER INFORMATION
# # ---------------------------------------------------------

# print("\nGenerating tower data...")

# NUM_TOWERS = 500

# regions = [
#     "North",
#     "South",
#     "East",
#     "West",
#     "Central"
# ]

# technologies = [
#     "4G",
#     "5G"
# ]

# tower_records = []

# for i in range(NUM_TOWERS):

#     tower_id = f"T{i + 1000}"

#     region = random.choice(regions)

#     technology = random.choice(technologies)

#     tower_records.append({
#         "tower_id": tower_id,
#         "region": region,
#         "technology": technology,
#         "latitude": round(random.uniform(8.0, 35.0), 6),
#         "longitude": round(random.uniform(68.0, 97.0), 6),
#         "installation_year": random.randint(2016, 2025)
#     })

# towers_df = pd.DataFrame(tower_records)

# tower_file = RAW_DATA_DIR / "towers.csv"

# towers_df.to_csv(tower_file, index=False)

# print(f"Created {len(towers_df)} towers")
# print("Saved:", tower_file)


# # ---------------------------------------------------------
# # 3. GENERATE NETWORK TELEMETRY
# # ---------------------------------------------------------

# print("\nGenerating network telemetry...")

# NUM_DAYS = 30

# start_date = datetime.now() - timedelta(days=NUM_DAYS)

# telemetry_records = []

# # Select towers that will intentionally experience degradation
# degraded_towers = set(
#     random.sample(
#         list(towers_df["tower_id"]),
#         25
#     )
# )

# print("Degraded towers:", len(degraded_towers))


# for day in range(NUM_DAYS):

#     current_date = start_date + timedelta(days=day)

#     for _, tower in towers_df.iterrows():

#         tower_id = tower["tower_id"]

#         # Generate 4 observations per day
#         for hour in [0, 6, 12, 18]:

#             timestamp = current_date + timedelta(hours=hour)

#             # ---------------------------------------------
#             # Normal network behavior
#             # ---------------------------------------------

#             active_users = max(
#                 50,
#                 int(np.random.normal(500, 100))
#             )

#             download_mbps = max(
#                 5,
#                 np.random.normal(120, 25)
#             )

#             upload_mbps = max(
#                 2,
#                 np.random.normal(35, 8)
#             )

#             latency_ms = max(
#                 5,
#                 np.random.normal(35, 8)
#             )

#             packet_loss_pct = max(
#                 0,
#                 np.random.normal(0.5, 0.2)
#             )

#             signal_strength_dbm = np.random.normal(
#                 -75,
#                 5
#             )

#             cpu_utilization_pct = np.clip(
#                 np.random.normal(55, 10),
#                 5,
#                 100
#             )

#             memory_utilization_pct = np.clip(
#                 np.random.normal(50, 8),
#                 5,
#                 100
#             )

#             call_drop_rate = max(
#                 0,
#                 np.random.normal(1.0, 0.4)
#             )

#             connection_failure_rate = max(
#                 0,
#                 np.random.normal(1.5, 0.5)
#             )

#             # ---------------------------------------------
#             # Inject degradation into selected towers
#             # ---------------------------------------------

#             if tower_id in degraded_towers:

#                 # Degradation becomes worse over time
#                 degradation_factor = (day + 1) / NUM_DAYS

#                 latency_ms += 100 * degradation_factor

#                 packet_loss_pct += 5 * degradation_factor

#                 signal_strength_dbm -= 15 * degradation_factor

#                 cpu_utilization_pct += 30 * degradation_factor

#                 call_drop_rate += 5 * degradation_factor

#                 connection_failure_rate += 7 * degradation_factor

#                 active_users = int(
#                     active_users * (1 - 0.25 * degradation_factor)
#                 )

#             telemetry_records.append({

#                 "timestamp": timestamp,

#                 "tower_id": tower_id,

#                 "active_users": active_users,

#                 "download_mbps": round(download_mbps, 2),

#                 "upload_mbps": round(upload_mbps, 2),

#                 "latency_ms": round(latency_ms, 2),

#                 "packet_loss_pct": round(
#                     packet_loss_pct,
#                     2
#                 ),

#                 "signal_strength_dbm": round(
#                     signal_strength_dbm,
#                     2
#                 ),

#                 "cpu_utilization_pct": round(
#                     min(cpu_utilization_pct, 100),
#                     2
#                 ),

#                 "memory_utilization_pct": round(
#                     memory_utilization_pct,
#                     2
#                 ),

#                 "call_drop_rate": round(
#                     call_drop_rate,
#                     2
#                 ),

#                 "connection_failure_rate": round(
#                     connection_failure_rate,
#                     2
#                 )
#             })


# telemetry_df = pd.DataFrame(
#     telemetry_records
# )

# telemetry_file = RAW_DATA_DIR / "network_telemetry.csv"

# telemetry_df.to_csv(
#     telemetry_file,
#     index=False
# )

# print(
#     f"Created {len(telemetry_df):,} telemetry records"
# )

# print("Saved:", telemetry_file)


# # ---------------------------------------------------------
# # 4. GENERATE FAULT EVENTS
# # ---------------------------------------------------------

# print("\nGenerating fault events...")

# fault_types = [
#     "Hardware Failure",
#     "Network Congestion",
#     "Power Issue",
#     "Backhaul Failure",
#     "Radio Degradation",
#     "Configuration Error"
# ]

# severities = [
#     "Low",
#     "Medium",
#     "High",
#     "Critical"
# ]

# fault_records = []

# NUM_FAULTS = 3000

# tower_ids = list(
#     towers_df["tower_id"]
# )

# for i in range(NUM_FAULTS):

#     tower_id = random.choice(tower_ids)

#     timestamp = start_date + timedelta(
#         minutes=random.randint(
#             0,
#             NUM_DAYS * 24 * 60
#         )
#     )

#     fault_type = random.choice(
#         fault_types
#     )

#     severity = random.choices(
#         severities,
#         weights=[40, 35, 20, 5]
#     )[0]

#     duration_minutes = max(
#         5,
#         int(np.random.exponential(60))
#     )

#     resolved = random.choices(
#         [True, False],
#         weights=[90, 10]
#     )[0]

#     fault_records.append({

#         "fault_id": f"F{i + 1:05d}",

#         "tower_id": tower_id,

#         "timestamp": timestamp,

#         "fault_type": fault_type,

#         "severity": severity,

#         "duration_minutes": duration_minutes,

#         "resolved": resolved
#     })


# faults_df = pd.DataFrame(
#     fault_records
# )

# fault_file = RAW_DATA_DIR / "tower_faults.csv"

# faults_df.to_csv(
#     fault_file,
#     index=False
# )

# print(
#     f"Created {len(faults_df):,} fault events"
# )

# print("Saved:", fault_file)


# # ---------------------------------------------------------
# # 5. GENERATE CUSTOMER INFORMATION
# # ---------------------------------------------------------

# print("\nGenerating customer data...")

# NUM_CUSTOMERS = 10000

# plans = [
#     "Basic",
#     "Standard",
#     "Premium",
#     "Unlimited"
# ]

# customer_records = []

# for i in range(NUM_CUSTOMERS):

#     tower_id = random.choice(tower_ids)

#     plan = random.choice(plans)

#     monthly_revenue = {
#         "Basic": 299,
#         "Standard": 499,
#         "Premium": 799,
#         "Unlimited": 1199
#     }[plan]

#     customer_records.append({

#         "customer_id": f"C{i + 10000}",

#         "tower_id": tower_id,

#         "region": towers_df.loc[
#             towers_df["tower_id"] == tower_id,
#             "region"
#         ].iloc[0],

#         "plan": plan,

#         "monthly_revenue": monthly_revenue,

#         "data_usage_gb": round(
#             max(
#                 0,
#                 np.random.normal(25, 10)
#             ),
#             2
#         ),

#         "complaint_count": random.choices(
#             [0, 1, 2, 3, 4],
#             weights=[65, 20, 8, 5, 2]
#         )[0]
#     })


# customers_df = pd.DataFrame(
#     customer_records
# )

# customer_file = RAW_DATA_DIR / "customers.csv"

# customers_df.to_csv(
#     customer_file,
#     index=False
# )

# print(
#     f"Created {len(customers_df):,} customers"
# )

# print("Saved:", customer_file)


# # ---------------------------------------------------------
# # 6. GENERATE NETWORK EVENTS
# # ---------------------------------------------------------

# print("\nGenerating network events...")

# event_types = [
#     "High Latency",
#     "Packet Loss",
#     "Call Drop",
#     "Connection Failure",
#     "High CPU",
#     "Low Signal",
#     "Traffic Spike"
# ]

# event_records = []

# NUM_EVENTS = 10000

# for i in range(NUM_EVENTS):

#     tower_id = random.choice(tower_ids)

#     timestamp = start_date + timedelta(
#         minutes=random.randint(
#             0,
#             NUM_DAYS * 24 * 60
#         )
#     )

#     event_type = random.choice(
#         event_types
#     )

#     severity = random.choices(
#         severities,
#         weights=[45, 35, 15, 5]
#     )[0]

#     event_records.append({

#         "event_id": f"E{i + 1:06d}",

#         "timestamp": timestamp,

#         "tower_id": tower_id,

#         "event_type": event_type,

#         "severity": severity
#     })


# events_df = pd.DataFrame(
#     event_records
# )

# events_file = RAW_DATA_DIR / "network_events.csv"

# events_df.to_csv(
#     events_file,
#     index=False
# )

# print(
#     f"Created {len(events_df):,} network events"
# )

# print("Saved:", events_file)


# # ---------------------------------------------------------
# # 7. FINAL SUMMARY
# # ---------------------------------------------------------

# print("\n" + "=" * 60)

# print("TELECOM DATA GENERATION COMPLETED")

# print("=" * 60)

# print(f"Towers:            {len(towers_df):,}")
# print(f"Telemetry records: {len(telemetry_df):,}")
# print(f"Fault events:      {len(faults_df):,}")
# print(f"Customers:         {len(customers_df):,}")
# print(f"Network events:    {len(events_df):,}")

# print("\nFiles created:")

# for file in RAW_DATA_DIR.iterdir():

#     print(
#         f" - {file.name}"
#     )

# print("\nAll raw data is available in:")

# print(RAW_DATA_DIR)




import pandas as pd
import numpy as np
from faker import Faker
from pathlib import Path
from datetime import datetime, timedelta
import random


# ============================================================
# 1. BASIC SETTINGS
# ============================================================

random.seed(42)
np.random.seed(42)

fake = Faker()
Faker.seed(42)


# ============================================================
# 2. PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

RAW_DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# 3. GENERAL SETTINGS
# ============================================================

NUM_TOWERS = 500
NUM_CUSTOMERS = 10000
NUM_FAULTS = 3000
NUM_EVENTS = 10000

NUM_DAYS = 30

REGIONS = [
    "North",
    "South",
    "East",
    "West",
    "Central"
]

TECHNOLOGIES = [
    "4G",
    "5G"
]


# ============================================================
# 4. GENERATE TOWERS
# ============================================================

print("\nGenerating tower data...")

tower_ids = [
    f"T{1000 + i}"
    for i in range(NUM_TOWERS)
]


towers = []

for tower_id in tower_ids:

    towers.append({

        "tower_id": tower_id,

        "region": random.choice(REGIONS),

        "technology": random.choice(TECHNOLOGIES),

        "latitude": round(
            random.uniform(8, 35),
            6
        ),

        "longitude": round(
            random.uniform(68, 97),
            6
        ),

        "installation_year": random.randint(
            2016,
            2025
        )

    })


towers_df = pd.DataFrame(towers)


towers_df.to_csv(
    RAW_DATA_DIR / "towers.csv",
    index=False
)


print(
    "Towers generated:",
    len(towers_df)
)


# ============================================================
# 5. SELECT DELIBERATELY DEGRADED TOWERS
# ============================================================

# These towers will gradually become worse over the
# 30-day period.

degraded_towers = set(
    random.sample(
        tower_ids,
        25
    )
)


print(
    "Deliberately degraded towers:",
    len(degraded_towers)
)


# ============================================================
# 6. GENERATE NETWORK TELEMETRY
# ============================================================

print("\nGenerating network telemetry...")


telemetry = []


start_date = datetime(
    2026,
    1,
    1,
    0,
    0,
    0
)


for day in range(NUM_DAYS):

    for tower_id in tower_ids:

        for hour in [0, 6, 12, 18]:

            timestamp = (
                start_date
                + timedelta(days=day)
                + timedelta(hours=hour)
            )


            # ------------------------------------------------
            # Normal network behavior
            # ------------------------------------------------

            active_users = max(
                20,
                int(
                    np.random.normal(
                        500,
                        120
                    )
                )
            )


            download_mbps = max(
                1,
                np.random.normal(
                    80,
                    15
                )
            )


            upload_mbps = max(
                1,
                np.random.normal(
                    25,
                    6
                )
            )


            latency_ms = max(
                5,
                np.random.normal(
                    45,
                    10
                )
            )


            packet_loss_pct = max(
                0,
                np.random.normal(
                    1.5,
                    0.7
                )
            )


            signal_strength_dbm = np.random.normal(
                -75,
                8
            )


            cpu_utilization_pct = np.clip(
                np.random.normal(
                    50,
                    12
                ),
                5,
                99
            )


            memory_utilization_pct = np.clip(
                np.random.normal(
                    55,
                    10
                ),
                5,
                99
            )


            call_drop_rate = max(
                0,
                np.random.normal(
                    1.5,
                    0.7
                )
            )


            connection_failure_rate = max(
                0,
                np.random.normal(
                    1.5,
                    0.7
                )
            )


            # ------------------------------------------------
            # DELIBERATE DEGRADATION
            # ------------------------------------------------

            if tower_id in degraded_towers:

                # As days increase, the tower becomes worse.

                degradation = (
                    day / (NUM_DAYS - 1)
                )


                # Latency increases

                latency_ms += (
                    100 * degradation
                )


                # Packet loss increases

                packet_loss_pct += (
                    6 * degradation
                )


                # Download speed decreases

                download_mbps -= (
                    40 * degradation
                )


                # Upload speed decreases

                upload_mbps -= (
                    12 * degradation
                )


                # Signal becomes weaker

                signal_strength_dbm -= (
                    25 * degradation
                )


                # CPU increases

                cpu_utilization_pct += (
                    40 * degradation
                )


                # Memory increases

                memory_utilization_pct += (
                    30 * degradation
                )


                # Call drops increase

                call_drop_rate += (
                    6 * degradation
                )


                # Connection failures increase

                connection_failure_rate += (
                    6 * degradation
                )


                # Active users decrease because
                # customers experience bad service.

                active_users -= int(
                    200 * degradation
                )


            # ------------------------------------------------
            # Keep values within realistic ranges
            # ------------------------------------------------

            active_users = max(
                0,
                int(active_users)
            )


            download_mbps = max(
                1,
                round(download_mbps, 2)
            )


            upload_mbps = max(
                1,
                round(upload_mbps, 2)
            )


            latency_ms = max(
                1,
                round(latency_ms, 2)
            )


            packet_loss_pct = np.clip(
                packet_loss_pct,
                0,
                100
            )


            signal_strength_dbm = np.clip(
                signal_strength_dbm,
                -120,
                -40
            )


            cpu_utilization_pct = np.clip(
                cpu_utilization_pct,
                0,
                100
            )


            memory_utilization_pct = np.clip(
                memory_utilization_pct,
                0,
                100
            )


            call_drop_rate = np.clip(
                call_drop_rate,
                0,
                100
            )


            connection_failure_rate = np.clip(
                connection_failure_rate,
                0,
                100
            )


            telemetry.append({

                "timestamp": timestamp,

                "tower_id": tower_id,

                "active_users": active_users,

                "download_mbps": round(
                    download_mbps,
                    2
                ),

                "upload_mbps": round(
                    upload_mbps,
                    2
                ),

                "latency_ms": round(
                    latency_ms,
                    2
                ),

                "packet_loss_pct": round(
                    packet_loss_pct,
                    2
                ),

                "signal_strength_dbm": round(
                    signal_strength_dbm,
                    2
                ),

                "cpu_utilization_pct": round(
                    cpu_utilization_pct,
                    2
                ),

                "memory_utilization_pct": round(
                    memory_utilization_pct,
                    2
                ),

                "call_drop_rate": round(
                    call_drop_rate,
                    2
                ),

                "connection_failure_rate": round(
                    connection_failure_rate,
                    2
                )

            })


telemetry_df = pd.DataFrame(
    telemetry
)


telemetry_df.to_csv(
    RAW_DATA_DIR / "network_telemetry.csv",
    index=False
)


print(
    "Telemetry records generated:",
    len(telemetry_df)
)


# ============================================================
# 7. GENERATE TOWER FAULTS
# ============================================================

print("\nGenerating tower fault data...")


faults = []


fault_types = [

    "Hardware Failure",

    "Network Congestion",

    "Power Issue",

    "Backhaul Failure",

    "Radio Degradation",

    "Configuration Error"

]


severities = [

    "Low",

    "Medium",

    "High",

    "Critical"

]


# ------------------------------------------------------------
# Approximately 100 towers will experience faults.
# The remaining towers will have no historical faults.
# ------------------------------------------------------------

fault_prone_towers = set(
    random.sample(
        tower_ids,
        75
    )
)


# Always include the deliberately degraded towers.

fault_prone_towers.update(
    degraded_towers
)


fault_prone_towers = list(
    fault_prone_towers
)


print(
    "Fault-prone towers:",
    len(fault_prone_towers)
)


# ------------------------------------------------------------
# Generate fault events
# ------------------------------------------------------------

for i in range(NUM_FAULTS):

    tower_id = random.choice(
        fault_prone_towers
    )


    fault_time = (

        start_date

        + timedelta(
            days=random.randint(
                0,
                NUM_DAYS - 1
            )
        )

        + timedelta(
            hours=random.choice(
                [0, 6, 12, 18]
            )
        )

    )


    fault_type = random.choice(
        fault_types
    )


    severity = random.choices(

        severities,

        weights=[
            40,
            35,
            20,
            5
        ],

        k=1

    )[0]


    duration_minutes = max(

        5,

        int(
            np.random.exponential(
                60
            )
        )

    )


    resolved = (
        random.random() < 0.90
    )


    faults.append({

        "fault_id": f"F{i + 1:05d}",

        "tower_id": tower_id,

        "timestamp": fault_time,

        "fault_type": fault_type,

        "severity": severity,

        "duration_minutes": duration_minutes,

        "resolved": resolved

    })


faults_df = pd.DataFrame(
    faults
)


faults_df.to_csv(
    RAW_DATA_DIR / "tower_faults.csv",
    index=False
)


print(
    "Fault records generated:",
    len(faults_df)
)


# ============================================================
# 8. GENERATE CUSTOMERS
# ============================================================

print("\nGenerating customer data...")


customers = []


plans = [

    "Basic",

    "Standard",

    "Premium",

    "Unlimited"

]


plan_revenue = {

    "Basic": 299,

    "Standard": 499,

    "Premium": 799,

    "Unlimited": 1199

}


for i in range(NUM_CUSTOMERS):

    customer_id = (
        f"C{i + 1:05d}"
    )


    tower_id = random.choice(
        tower_ids
    )


    region = towers_df.loc[
        towers_df["tower_id"] == tower_id,
        "region"
    ].iloc[0]


    plan = random.choice(
        plans
    )


    monthly_revenue = plan_revenue[
        plan
    ]


    data_usage_gb = max(

        0,

        round(
            np.random.normal(
                25,
                10
            ),
            2
        )

    )


    complaint_count = max(

        0,

        int(
            np.random.poisson(
                1
            )
        )

    )


    # Customers connected to degraded towers
    # are more likely to have complaints.

    if tower_id in degraded_towers:

        complaint_count += random.randint(
            1,
            5
        )


    customers.append({

        "customer_id": customer_id,

        "tower_id": tower_id,

        "region": region,

        "plan": plan,

        "monthly_revenue": monthly_revenue,

        "data_usage_gb": data_usage_gb,

        "complaint_count": complaint_count

    })


customers_df = pd.DataFrame(
    customers
)


customers_df.to_csv(
    RAW_DATA_DIR / "customers.csv",
    index=False
)


print(
    "Customers generated:",
    len(customers_df)
)


# ============================================================
# 9. GENERATE NETWORK EVENTS
# ============================================================

print("\nGenerating network events...")


events = []


event_types = [

    "High Latency",

    "Packet Loss",

    "Call Drop",

    "Connection Failure",

    "High CPU",

    "Low Signal",

    "Traffic Spike"

]


for i in range(NUM_EVENTS):

    tower_id = random.choice(
        tower_ids
    )


    event_time = (

        start_date

        + timedelta(
            days=random.randint(
                0,
                NUM_DAYS - 1
            )
        )

        + timedelta(
            hours=random.choice(
                [0, 6, 12, 18]
            )
        )

    )


    event_type = random.choice(
        event_types
    )


    severity = random.choices(

        severities,

        weights=[
            50,
            30,
            15,
            5
        ],

        k=1

    )[0]


    events.append({

        "event_id": f"E{i + 1:05d}",

        "timestamp": event_time,

        "tower_id": tower_id,

        "event_type": event_type,

        "severity": severity

    })


events_df = pd.DataFrame(
    events
)


events_df.to_csv(
    RAW_DATA_DIR / "network_events.csv",
    index=False
)


print(
    "Network events generated:",
    len(events_df)
)


# ============================================================
# 10. FINAL SUMMARY
# ============================================================

print("\n")
print("================================================")
print("        TELECOM DATA GENERATION COMPLETE")
print("================================================")

print(
    "\nRaw data location:"
)

print(
    RAW_DATA_DIR
)


print("\nGenerated files:")

print(
    "1. towers.csv"
)

print(
    "2. network_telemetry.csv"
)

print(
    "3. tower_faults.csv"
)

print(
    "4. customers.csv"
)

print(
    "5. network_events.csv"
)


print("\nRecord counts:")

print(
    "Towers:",
    len(towers_df)
)

print(
    "Telemetry:",
    len(telemetry_df)
)

print(
    "Faults:",
    len(faults_df)
)

print(
    "Customers:",
    len(customers_df)
)

print(
    "Network events:",
    len(events_df)
)


print("\nData generation finished successfully!")
