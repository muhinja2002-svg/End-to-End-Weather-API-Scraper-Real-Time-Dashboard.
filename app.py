import streamlit as st
import pandas as pd
import requests

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="Global Weather Analytics Platform",
    page_icon="🌍",
    layout="wide"
)

# 2. API CONFIGURATION (Securely pulling from Streamlit Secrets)
SUPABASE_URL = "https://ahnotyrkehippbomgvop.supabase.co"
try:
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
except KeyError:
    st.error("Missing SUPABASE_KEY. Please add it to your .streamlit/secrets.toml or Streamlit Cloud settings.")
    st.stop()

# 3. COORDINATE LOOKUP
coords = {
    "Nairobi": {"lat": -1.286389, "lon": 36.817223},
    "London": {"lat": 51.5074, "lon": -0.1278},
    "Sydney": {"lat": -33.8688, "lon": 151.2093},
    "Tokyo": {"lat": 35.6895, "lon": 139.6917},
    "New York": {"lat": 40.7128, "lon": -74.0060}
}

# 4. DATA FETCHING FUNCTION
@st.cache_data(ttl=3600)  # Refresh cache every hour
def load_data():
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
    url = f"{SUPABASE_URL}/rest/v1/weather_metrics?select=*"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except Exception as e:
        st.error(f"Error connecting to Supabase: {e}")
        return pd.DataFrame()

# --- DASHBOARD UI ---

st.title("🌍 Real-Time Weather Data Analytics")
st.markdown(f"**Status:** Live Connection to Supabase Cloud | **Security:** Active (Streamlit Secrets)")
st.divider()

df = load_data()

if not df.empty:
    # Data Preparation
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Apply Coordinates
    df['lat'] = df['city'].map(lambda x: coords.get(x, {}).get('lat'))
    df['lon'] = df['city'].map(lambda x: coords.get(x, {}).get('lon'))

    # ROW 1: Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Records", len(df))
    # We round to 1 decimal place for clean business reporting
    col2.metric("Avg Global Temp", f"{round(df['temperature_c'].mean(), 1)}°C")
    col3.metric("Avg Humidity", f"{round(df['humidity_pct'].mean(), 1)}%")
    col4.metric("Cities Tracked", df['city'].nunique())

    # ROW 2: Map Visualization
    st.subheader("📍 Global Reading Locations")
    map_df = df.dropna(subset=['lat', 'lon'])
    st.map(map_df)

    # ROW 3: Trends & Comparison
    st.divider()
    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader("Temperature Trends")
        # Creating a pivot for a clean time-series line chart
        chart_data = df.pivot_table(index='timestamp', columns='city', values='temperature_c')
        st.line_chart(chart_data)

    with right_col:
        st.subheader("Recent Activity Log")
        st.dataframe(
            df[['timestamp', 'city', 'temperature_c', 'status']].sort_values('timestamp', ascending=False),
            use_container_width=True,
            hide_index=True
        )
else:
    st.info("No data found. Ensure your GitHub Action has run successfully.")