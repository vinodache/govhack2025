
import pandas as pd
from collections import defaultdict
import json
import os


files_to_process = [
    ("./govhack2025/Data/20251496-Rawdata-July-20251-Geelong.ods", "Area_2025.json", "Sheet1"),
    ("./govhack2025/Data/20240067-Raw-Data-December-2023-Geelong.ods", "Area_2023.json", "Data"),
    ("./govhack2025/Data/December-2022-Raw-data-Geelong.ods", "Area_2022.json", "data"),
    ("./govhack2025/Data/VBA-DataVic-Building-Permits-2021-Dec-Geelong.ods", "Area_2021.json", "Sheet1"),
    ("./govhack2025/Data/VBA-DataVic-Building-Permits-2020-Geelong.ods", "Area_2020.json", "Sheet1"),
]


# Write Area_*.json files into the Data folder relative to this script
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = script_dir

for file_path, output_json, sheet_name in files_to_process:
    if not os.path.exists(file_path):
        print(f"File not found: {file_path} (skipping)")
        continue
    print(f"Processing {file_path} -> {output_json} (sheet: {sheet_name})")
    df = pd.read_excel(file_path, engine="odf", sheet_name=sheet_name)
    grouped = defaultdict(lambda: {"AllotmentArea": 0, "ExistingDwelling": 0, "NewDwellings": 0})
    for _, row in df.iterrows():
        suburb = row.get("site_town_suburb__c")
        if pd.isna(suburb):
            continue
        suburb_upper = str(suburb).strip().upper()
        # Safely convert values to float, treat non-numeric as 0
        def safe_float(val):
            try:
                return float(val)
            except (TypeError, ValueError):
                return 0.0
        grouped[suburb_upper]["AllotmentArea"] += safe_float(row.get("Allotment_Area__c", 0)) if not pd.isna(row.get("Allotment_Area__c")) else 0
        grouped[suburb_upper]["ExistingDwelling"] += safe_float(row.get("Number_of_Existing_Dwellings__c", 0)) if not pd.isna(row.get("Number_of_Existing_Dwellings__c")) else 0
        grouped[suburb_upper]["NewDwellings"] += safe_float(row.get("Number_of_New_Dwellings__c", 0)) if not pd.isna(row.get("Number_of_New_Dwellings__c")) else 0
    output_path = os.path.join(data_dir, output_json)
    with open(output_path, "w") as f:
        json.dump(grouped, f, indent=2)
    print(f"{output_path} created.")
