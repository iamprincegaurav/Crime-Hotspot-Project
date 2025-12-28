import pandas as pd
import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("data/crime_data.csv")
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Month'] = df['Date'].dt.month

st.title("Crime Hotspot & Pattern Analysis Dashboard - Patna City")

# Sidebar filters
crime_types = st.sidebar.multiselect("Select Crime Types:", df['Crime_Type'].unique(), default=df['Crime_Type'].unique())
months = st.sidebar.multiselect("Select Month(s):", sorted(df['Month'].unique()), default=sorted(df['Month'].unique()))

filtered_df = df[df['Crime_Type'].isin(crime_types) & df['Month'].isin(months)]

# --- Crime Type Frequency Bar Chart ---
st.subheader("Crime Type Frequency")
fig, ax = plt.subplots(figsize=(10,4))
sns.countplot(x='Crime_Type', data=filtered_df, order=filtered_df['Crime_Type'].value_counts().index, palette="Set2", ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# --- Monthly Trend ---
st.subheader("Monthly Crime Trend")
monthly_trend = filtered_df.groupby('Month')['Crime_Type'].count()
fig2, ax2 = plt.subplots(figsize=(10,4))
ax2.plot(monthly_trend.index, monthly_trend.values, marker='o', color='orange')
ax2.set_xlabel("Month")
ax2.set_ylabel("Number of Crimes")
ax2.set_title("Monthly Crime Trend")
ax2.grid(True)
st.pyplot(fig2)

# --- Folium Map with Heatmap + Color Dots ---
st.subheader("Crime Hotspot Map")
m = folium.Map(location=[25.5941, 85.1376], zoom_start=12)

# Color coding for Crime Types
crime_colors = {
    "Murder": "black",
    "Theft": "red",
    "Assault": "orange",
    "Robbery": "purple",
    "Vehicle Theft": "blue",
    "Burglary": "green",
    "Chain Snatching": "yellow",
    "Riot": "darkred"
}

# Add circle markers
for _, row in filtered_df.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=6,
        popup=f"{row['Crime_Type']} at {row['Location']}",
        color=crime_colors.get(row['Crime_Type'], "gray"),
        fill=True,
        fill_color=crime_colors.get(row['Crime_Type'], "gray"),
        fill_opacity=0.7
    ).add_to(m)

# HeatMap layer
heat_data = [[row['Latitude'], row['Longitude']] for _, row in filtered_df.iterrows()]
HeatMap(heat_data, radius=25).add_to(m)

folium_static(m)
