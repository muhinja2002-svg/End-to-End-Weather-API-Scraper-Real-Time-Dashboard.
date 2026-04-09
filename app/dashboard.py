import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="Live Weather Ops", page_icon="🌦️", layout="wide")

@st.cache_data(ttl=60) # Auto-updates cache every 60 seconds
def load_data():
    try:
        conn = sqlite3.connect('data/weather.db')
        query = "SELECT * FROM weather_logs ORDER BY timestamp DESC"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error("Database not found. Please run the ETL pipeline first.")
        return pd.DataFrame()

st.title("🌦️ Global Weather Operations Center")
st.markdown("Monitoring real-time meteorological conditions for logistics routing.")

df = load_data()

if not df.empty:
    # KPI Metrics
    col1, col2, col3 = st.columns(3)
    latest_record = df.iloc[0]
    
    col1.metric("Latest Update", latest_record['city'], latest_record['timestamp'][:16])
    col2.metric("Current Temp (Avg)", f"{df['temperature_c'].mean():.1f} °C")
    col3.metric("Records Ingested", len(df))

    # Data Visualization
    st.subheader("Temperature Trends by City")
    st.line_chart(df.pivot(index='timestamp', columns='city', values='temperature_c'))

    # Raw Data Table
    st.subheader("Raw Telemetry (Latest 50)")
    st.dataframe(df.head(50), use_container_width=True)
else:
    st.warning("No data available. Pipeline may be running or failed.")