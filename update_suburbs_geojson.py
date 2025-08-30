import json

# Load Area_2025.json
with open("/Users/uma/govhack2025/Area_2025.json") as f:
    area_data = json.load(f)

# Load suburbs.geojson
with open("/Users/uma/govhack2025/govhack2025/suburbs.geojson") as f:
    geojson = json.load(f)

# Update each feature's properties
for feature in geojson.get("features", []):
    loc_name = feature.get("properties", {}).get("loc_name", "").upper()
    if loc_name in area_data:
        feature["properties"]["AllotmentArea"] = area_data[loc_name]["AllotmentArea"]
        feature["properties"]["ExistingDwelling"] = area_data[loc_name]["ExistingDwelling"]
        feature["properties"]["NewDwellings"] = area_data[loc_name]["NewDwellings"]

# Save to a new file
with open("/Users/uma/govhack2025/govhack2025/suburbs_updated.geojson", "w") as f:
    json.dump(geojson, f, indent=2)

print("suburbs_updated.geojson created.")
