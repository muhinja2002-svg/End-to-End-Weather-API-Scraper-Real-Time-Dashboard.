# 🌦️ Real-Time Weather Data Platform

## 🎯 The "So What?" (Business Value)
Supply chain and logistics teams lose millions annually due to unpredicted extreme weather events. This platform ingests real-time telemetry from external meteorological APIs, validates data to prevent silent downstream reporting failures, and visualizes it in an auto-updating dashboard. This allows operational teams to reroute shipments proactively based on live weather fronts.

## 🚀 The "Juja-to-Cloud" Architecture
To overcome local network latency and TCP timeouts in Kisumu, the pipeline was migrated from a local runner to a fully cloud-native architecture. 

```mermaid
graph LR
    A[OpenWeather API] --> B[GitHub Actions Runner]
    B --> C{Pydantic Validation}
    C -->|Validated| D[(Supabase Postgres)]
    D --> E[Streamlit Dashboard]
    C -->|Failure| F[Action Logs]

    style D fill:#3ecf8e,stroke:#333,color:#fff
    style B fill:#24292e,stroke:#333,color:#fff
    style E fill:#ff4b4b,stroke:#333,color:#fff
