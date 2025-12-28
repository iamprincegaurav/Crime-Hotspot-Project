import pandas as pd
import folium
from folium.plugins import HeatMap

# Load dataset
df = pd.read_csv("data/crime_data.csv")
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Create base map (Patna)
m = folium.Map(location=[25.5941, 85.1376], zoom_start=12)

# --- Color coding for Crime Types ---
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

# Add colored circle markers
for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=6,
        popup=f"{row['Crime_Type']} at {row['Location']}",
        color=crime_colors.get(row['Crime_Type'], "gray"),
        fill=True,
        fill_color=crime_colors.get(row['Crime_Type'], "gray"),
        fill_opacity=0.7
    ).add_to(m)

# --- HeatMap layer for density ---
heat_data = [[row['Latitude'], row['Longitude']] for index, row in df.iterrows()]
HeatMap(heat_data, radius=25).add_to(m)

# Save map
m.save("crime_hotspot_map_advanced.html")
print("Advanced Crime Hotspot Map generated! Open 'crime_hotspot_map_advanced.html' in browser.")
