# Telecom Network Intelligence & Predictive Failure Analytics

An end-to-end telecom analytics platform that monitors tower health, detects network anomalies, predicts tower failure risk, and identifies potential customer and revenue impact.

## Features

- Telecom network data generation and processing
- Bronze, Silver, and Gold data layers
- Data cleaning and validation
- Tower health scoring
- Network anomaly detection using Isolation Forest
- Tower failure risk prediction using Random Forest
- Customer and revenue impact analysis
- Interactive Streamlit dashboard

## Tech Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- CSV / Parquet
- Git & GitHub

## Architecture

```text
Telecom Data
     ↓
Data Validation & Cleaning
     ↓
Bronze → Silver → Gold
     ↓
Analytics & Anomaly Detection
     ↓
Failure Risk Prediction
     ↓
Customer Impact Analysis
     ↓
Streamlit Dashboard
