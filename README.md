# 🌍 Real-Time Weather Data Platform

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![GitHub Actions](https://img.shields.io/badge/automation-GitHub%20Actions-orange)
![Database](https://img.shields.io/badge/database-Supabase%20PostgreSQL-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

## 🎯 The "So What?" (Business Value)
Supply chain and logistics teams lose millions annually due to unpredicted extreme weather events. This platform ingests real-time telemetry from external meteorological APIs, validates data to prevent silent downstream reporting failures, and visualizes it in an auto-updating dashboard. This allows operational teams to reroute shipments proactively based on live weather fronts.

## 🚀 The "Juja-to-Cloud" Architecture
To overcome local network latency and TCP timeouts often encountered in local development environments, the pipeline was migrated from a local runner to a **fully cloud-native, serverless architecture**.



### 1. Ingestion (Extract)
* **Tech:** Python, OpenWeatherMap API.
* **Logic:** A resilient script fetches current weather telemetry for 5 global cities. It includes custom timeout handling and error logging to ensure pipeline stability.

### 2. Validation & Transformation (Transform)
* **Tech:** Pydantic v2.
* **Logic:** Data is enforced against a strict schema. We implement range validation (e.g., Humidity must be 0-100%) to ensure "garbage in, garbage out" is prevented before reaching the database.

### 3. Persistence (Load)
* **Tech:** Supabase (PostgreSQL).
* **Logic:** Implemented **Idempotent Upserts**. Using a custom `merge-duplicates` header, the system ensures that if a reading is fetched twice, the database merges them rather than creating duplicates, preserving data integrity.

### 4. Automation (Orchestration)
* **Tech:** GitHub Actions.
* **Logic:** The ETL process is containerized and scheduled to run every hour via cron, creating a hands-free, self-sustaining data product.

### 5. Visualization (Analytics)
* **Tech:** Streamlit Cloud.
* **Logic:** A live dashboard connected via secure environment secrets to provide real-time KPIs on global temperature averages and reading distribution.

## 🛠️ Tech Stack
* **Language:** Python 3.11
* **Validation:** Pydantic
* **Database:** PostgreSQL (Supabase)
* **CI/CD:** GitHub Actions
* **Dashboard:** Streamlit

## 🔐 Security
This project follows professional security protocols:
* **Zero-Hardcoding Policy:** All API keys and database credentials are managed via GitHub Repository Secrets and Streamlit Secrets.
* **Environment Isolation:** Local development uses `.env` and `.streamlit/secrets.toml`, both of which are strictly excluded via `.gitignore`.

## 📈 Future Roadmap
- [ ] Add Time-Series forecasting using Prophet or ARIMA.
- [ ] Implement unit tests using `pytest` for schema validation.
- [ ] Add an automated email alerting system for extreme weather thresholds.
