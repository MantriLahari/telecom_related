import streamlit as st
import pandas as pd
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Telecom Network Intelligence",
    page_icon="📡",
    layout="wide"
)


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

GOLD_DIR = PROJECT_ROOT / "data" / "gold"


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    tower_health = pd.read_csv(
        GOLD_DIR / "tower_health.csv"
    )

    predictions = pd.read_csv(
        GOLD_DIR / "tower_failure_predictions.csv"
    )

    anomalies = pd.read_csv(
        GOLD_DIR / "tower_anomaly_detection.csv"
    )

    customer_impact = pd.read_csv(
        GOLD_DIR / "customer_impact.csv"
    )

    regional_impact = pd.read_csv(
        GOLD_DIR / "regional_customer_impact.csv"
    )

    tower_customer_impact = pd.read_csv(
        GOLD_DIR / "tower_customer_impact.csv"
    )

    return (
        tower_health,
        predictions,
        anomalies,
        customer_impact,
        regional_impact,
        tower_customer_impact
    )


try:

    (
        tower_health,
        predictions,
        anomalies,
        customer_impact,
        regional_impact,
        tower_customer_impact
    ) = load_data()

except Exception as e:

    st.error(
        "Unable to load project data."
    )

    st.exception(e)

    st.stop()


# ============================================================
# HEADER
# ============================================================

st.title("📡 Telecom Network Intelligence Platform")

st.markdown(
    """
    **Predictive Network Monitoring & Failure Analytics**

    Monitor tower health, identify anomalies, predict tower failures,
    and estimate customer and revenue impact.
    """
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Module",
    [
        "Executive Overview",
        "Tower Monitoring",
        "Failure Prediction",
        "Customer Impact",
        "Root Cause Analysis"
    ]
)


# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

if page == "Executive Overview":

    st.header("Executive Overview")

    total_towers = tower_health["tower_id"].nunique()

    critical_towers = predictions[
        predictions["risk_category"].isin(
            ["HIGH", "CRITICAL"]
        )
    ]["tower_id"].nunique()

    affected_customers = int(
        customer_impact[
            "potentially_affected"
        ].sum()
    )

    revenue_at_risk = customer_impact[
        "revenue_at_risk"
    ].sum()

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Towers",
        f"{total_towers:,}"
    )

    col2.metric(
        "High/Critical Towers",
        f"{critical_towers:,}"
    )

    col3.metric(
        "Affected Customers",
        f"{affected_customers:,}"
    )

    col4.metric(
        "Monthly Revenue at Risk",
        f"${revenue_at_risk:,.0f}"
    )

    st.divider()

    # --------------------------------------------------------
    # TOWER HEALTH
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Tower Health Distribution")

        health_distribution = (
            tower_health[
                "tower_status"
            ]
            .value_counts()
            .reset_index()
        )

        health_distribution.columns = [
            "Status",
            "Towers"
        ]

        st.bar_chart(
            health_distribution.set_index("Status")
        )

    with col2:

        st.subheader("Failure Risk Distribution")

        risk_distribution = (
            predictions[
                "risk_category"
            ]
            .value_counts()
            .reset_index()
        )

        risk_distribution.columns = [
            "Risk",
            "Towers"
        ]

        st.bar_chart(
            risk_distribution.set_index("Risk")
        )

    # --------------------------------------------------------
    # REGIONAL IMPACT
    # --------------------------------------------------------

    st.subheader(
        "Revenue at Risk by Region"
    )

    region_chart = regional_impact[
        [
            "network_region",
            "revenue_at_risk"
        ]
    ].copy()

    region_chart = region_chart.set_index(
        "network_region"
    )

    st.bar_chart(region_chart)


# ============================================================
# TOWER MONITORING
# ============================================================

elif page == "Tower Monitoring":

    st.header("🗼 Tower Monitoring")

    st.write(
        "Search and inspect individual telecom towers."
    )

    tower_ids = sorted(
        tower_health["tower_id"].unique()
    )

    selected_tower = st.selectbox(
        "Select Tower",
        tower_ids
    )

    tower_info = tower_health[
        tower_health["tower_id"] == selected_tower
    ]

    prediction_info = predictions[
        predictions["tower_id"] == selected_tower
    ]

    if not tower_info.empty:

        health_row = tower_info.iloc[0]

        prediction_row = prediction_info.iloc[0]

        st.divider()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Tower Health Score",
            f"{health_row['tower_health_score']:.1f}"
        )

        col2.metric(
            "Failure Probability",
            f"{prediction_row['failure_probability']:.1f}%"
        )

        col3.metric(
            "Risk Category",
            prediction_row["risk_category"]
        )

        col4.metric(
            "Region",
            health_row["region"]
        )

        st.divider()

        st.subheader("Tower Information")

        information = pd.DataFrame({
            "Attribute": [
                "Tower ID",
                "Region",
                "Technology",
                "Health Score",
                "Tower Status",
                "Failure Probability",
                "Risk Category",
                "Recommended Action"
            ],

            "Value": [
                selected_tower,
                health_row["region"],
                health_row["technology"],
                health_row["tower_health_score"],
                health_row["tower_status"],
                prediction_row["failure_probability"],
                prediction_row["risk_category"],
                prediction_row["recommended_action"]
            ]
        })

        st.table(information)


# ============================================================
# FAILURE PREDICTION
# ============================================================

elif page == "Failure Prediction":

    st.header("🔮 Tower Failure Prediction")

    st.write(
        "Towers are ranked according to predicted failure risk."
    )

    risk_filter = st.multiselect(
        "Filter by Risk Category",
        ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
        default=["HIGH", "CRITICAL"]
    )

    filtered_predictions = predictions[
        predictions["risk_category"].isin(
            risk_filter
        )
    ].copy()

    filtered_predictions = filtered_predictions.sort_values(
        "failure_probability",
        ascending=False
    )

    st.dataframe(
        filtered_predictions[
            [
                "tower_id",
                "failure_probability",
                "risk_category",
                "recommended_action"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# CUSTOMER IMPACT
# ============================================================

elif page == "Customer Impact":

    st.header("👥 Customer Impact Analysis")

    total_customers = len(
        customer_impact
    )

    affected_customers = int(
        customer_impact[
            "potentially_affected"
        ].sum()
    )

    revenue_at_risk = customer_impact[
        "revenue_at_risk"
    ].sum()

    high_value_customers = int(
        customer_impact[
            "high_value_at_risk"
        ].sum()
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Customers",
        f"{total_customers:,}"
    )

    col2.metric(
        "Affected Customers",
        f"{affected_customers:,}"
    )

    col3.metric(
        "Revenue at Risk",
        f"${revenue_at_risk:,.0f}"
    )

    col4.metric(
        "High-Value Customers at Risk",
        f"{high_value_customers:,}"
    )

    st.divider()

    st.subheader(
        "Customer Impact by Region"
    )

    regional_chart = regional_impact[
        [
            "network_region",
            "affected_customers"
        ]
    ].copy()

    regional_chart = regional_chart.set_index(
        "network_region"
    )

    st.bar_chart(
        regional_chart
    )

    st.subheader(
        "Tower-Level Customer Impact"
    )

    st.dataframe(
        tower_customer_impact.sort_values(
            "revenue_at_risk",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# ROOT CAUSE ANALYSIS
# ============================================================

elif page == "Root Cause Analysis":

    st.header("🔍 Root Cause Analysis")

    st.write(
        "Identify network indicators associated with poor tower health."
    )

    selected_tower = st.selectbox(
        "Select Tower",
        sorted(
            tower_health["tower_id"].unique()
        )
    )

    tower = tower_health[
        tower_health["tower_id"] == selected_tower
    ]

    prediction = predictions[
        predictions["tower_id"] == selected_tower
    ]

    if not tower.empty:

        tower = tower.iloc[0]
        prediction = prediction.iloc[0]

        st.subheader(
            f"Tower {selected_tower}"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Health Score",
                f"{tower['tower_health_score']:.1f}"
            )

            st.metric(
                "Failure Probability",
                f"{prediction['failure_probability']:.1f}%"
            )

        with col2:

            st.metric(
                "Status",
                tower["tower_status"]
            )

            st.metric(
                "Risk",
                prediction["risk_category"]
            )

        st.divider()

        st.subheader(
            "Problem Indicators"
        )

        indicators = str(
            tower["problem_indicators"]
        )

        if indicators.lower() in [
            "none",
            "",
            "nan"
        ]:

            st.success(
                "No major problem indicators detected."
            )

        else:

            indicator_list = [
                x.strip()
                for x in indicators.split(",")
            ]

            for indicator in indicator_list:

                st.warning(
                    f"⚠️ {indicator}"
                )

        st.divider()

        st.subheader(
            "Recommended Action"
        )

        st.info(
            prediction["recommended_action"]
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Telecom Network Intelligence & Predictive Failure Analytics Platform"
)
