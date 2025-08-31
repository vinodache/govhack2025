import pandas as pd
from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from odf.text import P
import json
import os

# Input and output paths
ods_path = os.path.join('Data', 'DisadvantageSuburbs_Victoria.ods')
json_path = os.path.join('Data', 'DisadvantageSuburbs_Victoria.json')

def extract_disadvantage_data(ods_path):
    doc = load(ods_path)
    sheet = doc.spreadsheet.getElementsByType(Table)[0]
    data = []
    for i, row in enumerate(sheet.getElementsByType(TableRow)):
        cells = row.getElementsByType(TableCell)
        values = []
        for cell in cells:
            text_content = ''
            for p in cell.getElementsByType(P):
                text_content += str(p)
            values.append(text_content.strip())
        # Skip header row
        if i == 0:
            continue
        # Columns: B=1, D=3, K=10 (0-based)
        if len(values) > 10:
            try:
                data.append({
                    'suburb_name': values[1],
                    'Disadvantage_rank_VIC': values[10],
                    'Disadvantage_Score': values[3]
                })
            except Exception:
                continue
    return data

if __name__ == "__main__":
    disadvantage = extract_disadvantage_data(ods_path)
    with open(json_path, 'w') as f:
        json.dump(disadvantage, f, indent=2)
    print(f"Extracted {len(disadvantage)} records to {json_path}")
