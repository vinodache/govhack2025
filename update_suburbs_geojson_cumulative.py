import json
import os

# Paths
script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, "suburbs_updated_with_dates.geojson")
output_path = os.path.join(script_dir, "suburbs_updated_with_dates_latest.geojson")

# Years in order
years = ["2020", "2021", "2022", "2023", "2025"]

# Load the original file
with open(input_path) as f:
    geojson = json.load(f)

# Update ExistingDwelling cumulatively using original values
for feature in geojson.get("features", []):
    date_data = feature.get("properties", {}).get("date", {})
    # Store original values before updating
    original = {y: date_data[y]["ExistingDwelling"] for y in years if y in date_data and "ExistingDwelling" in date_data[y]}
    for idx, y in enumerate(years):
        if y in date_data and "ExistingDwelling" in date_data[y]:
            # Sum from original values only
            cumulative = sum(original[yy] for yy in years[:idx+1] if yy in original)
            date_data[y]["ExistingDwelling"] = cumulative

# Save to new file
with open(output_path, "w") as f:
    json.dump(geojson, f, indent=2)

print("suburbs_updated_with_dates_latest.geojson created.")
