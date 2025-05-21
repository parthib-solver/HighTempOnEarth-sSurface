import requests
import csv
import json
import os
import geopandas as gpd
from shapely.geometry import Point

# FIRMS CSV URL (MODIS Global, past 24h)
FIRMS_CSV_URL = "https://firms.modaps.eosdis.nasa.gov/data/active_fire/modis-c6.1/csv/MODIS_C6_1_Global_24h.csv"


# Output
os.makedirs("data", exist_ok=True)
json_path = "data/high_temp_hotspots.json"
geojson_path = "data/high_temp_hotspots.geojson"

print("🔽 Downloading FIRMS MODIS 24h CSV data...")
response = requests.get(FIRMS_CSV_URL)
response.raise_for_status()

decoded = response.content.decode('utf-8').splitlines()
reader = csv.DictReader(decoded)

temp = 400

hotspots = []
for row in reader:
    try:
        brightness = float(row["brightness"])
        if brightness <= temp:
            continue

        hotspot = {
            "latitude": float(row["latitude"]),
            "longitude": float(row["longitude"]),
            "brightness": brightness,
            "confidence": row.get("confidence"),
            "acq_date": row.get("acq_date"),
            "acq_time": row.get("acq_time"),
            "satellite": row.get("satellite")
        }
        hotspots.append(hotspot)
    except Exception as e:
        print(f"⚠️ Skipped row due to error: {e}")

print(f"🔥 Found {len(hotspots)} hotspots > {temp}")

# Save as JSON
with open(json_path, "w") as f:
    json.dump(hotspots, f, indent=2)
print(f"💾 Saved JSON to {json_path}")

# Convert to GeoJSON
gdf = gpd.GeoDataFrame(
    hotspots,
    geometry=[Point(h["longitude"], h["latitude"]) for h in hotspots],
    crs="EPSG:4326"
)
gdf.to_file(geojson_path, driver="GeoJSON")
print(f"🗺️ Saved GeoJSON to {geojson_path}")
