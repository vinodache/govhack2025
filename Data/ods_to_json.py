import pandas as pd
from collections import defaultdict
import json

# Read the ODS file (first sheet)
file_path = "./govhack2025/Data/20251496-Rawdata-July-20251-Geelong.ods"
df = pd.read_excel(file_path, engine="odf", sheet_name="Sheet1")

# Prepare the aggregation
grouped = defaultdict(lambda: {"AllotmentArea": 0, "ExistingDwelling": 0, "NewDwellings": 0})

for _, row in df.iterrows():
    suburb = row.get("site_town_suburb__c")
    if pd.isna(suburb):
        # print(f"suburb: {suburb}")
        continue
    suburb_upper = str(suburb).strip().upper()
    # print(f"suburb: {suburb} -> {suburb_upper}")
    grouped[suburb_upper]["AllotmentArea"] += row.get("Allotment_Area__c", 0) if not pd.isna(row.get("Allotment_Area__c")) else 0
    grouped[suburb_upper]["ExistingDwelling"] += row.get("Number_of_Existing_Dwellings__c", 0) if not pd.isna(row.get("Number_of_Existing_Dwellings__c")) else 0
    grouped[suburb_upper]["NewDwellings"] += row.get("Number_of_New_Dwellings__c", 0) if not pd.isna(row.get("Number_of_New_Dwellings__c")) else 0
    # print(f"grouped: {dict(grouped)}\n")

# Write to JSON
with open("Area_2025.json", "w") as f:
    json.dump(grouped, f, indent=2)

print("Area_2025.json created.")
