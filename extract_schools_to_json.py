import pandas as pd
from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from odf.text import P
import json
import os

# Input and output paths
ods_path = os.path.join('Data', 'dv402-SchoolLocations2025-Geelong.ods')
json_path = 'schools_geelong.json'

def extract_school_data(ods_path):
    doc = load(ods_path)
    sheet = doc.spreadsheet.getElementsByType(Table)[0]
    data = []
    headers = []
    for i, row in enumerate(sheet.getElementsByType(TableRow)):
        cells = row.getElementsByType(TableCell)
        values = []
        for cell in cells:
            text_content = ''
            for p in cell.getElementsByType(P):
                text_content += str(p)
            values.append(text_content.strip())
        if i == 0:
            headers = values
        else:
            if len(values) < 3:
                continue
            row_dict = dict(zip(headers, values))
            # Only add if all required fields are present
            if 'School_Name' in row_dict and 'X' in row_dict and 'Y' in row_dict:
                try:
                    data.append({
                        'School_Name': row_dict['School_Name'],
                        'longitude': float(row_dict['X']),
                        'latitude': float(row_dict['Y'])
                    })
                except ValueError:
                    continue
    return data

if __name__ == "__main__":
    schools = extract_school_data(ods_path)
    with open(json_path, 'w') as f:
        json.dump(schools, f, indent=2)
    print(f"Extracted {len(schools)} schools to {json_path}")
