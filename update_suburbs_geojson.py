import json

# Load all Area_YEAR.json files
import os

# Use paths relative to this script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
years = [2025, 2023, 2022, 2021, 2020]
area_data_by_year = {}
for year in years:
    path = os.path.join(script_dir, "..", "Data", f"Area_{year}.json")
    if os.path.exists(path):
        with open(path) as f:
            area_data_by_year[str(year)] = json.load(f)
    else:
        area_data_by_year[str(year)] = {}

# Load suburbs.geojson
suburbs_geojson_path = os.path.join(script_dir, "suburbs.geojson")
with open(suburbs_geojson_path) as f:
    geojson = json.load(f)

# Update each feature's properties with nested date attributes
for feature in geojson.get("features", []):
    loc_name = feature.get("properties", {}).get("loc_name", "").upper()
    date_dict = {}
    for year in years:
        year_str = str(year)
        area_data = area_data_by_year[year_str]
        if loc_name in area_data:
            date_dict[year_str] = {
                "AllotmentArea": area_data[loc_name]["AllotmentArea"],
                "ExistingDwelling": area_data[loc_name]["ExistingDwelling"],
                "NewDwellings": area_data[loc_name]["NewDwellings"]
            }
    if date_dict:
        feature["properties"]["date"] = date_dict


# Save to a new file
output_path = os.path.join(script_dir, "suburbs_updated_with_dates.geojson")
with open(output_path, "w") as f:
    json.dump(geojson, f, indent=2)

print("suburbs_updated_with_dates.geojson created.")
