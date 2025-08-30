import pandas as pd

file_path = "./govhack2025/Data/20251496-Rawdata-July-20251-Geelong.ods"
df = pd.read_excel(file_path, engine="odf", sheet_name="Sheet1")

print("Columns:")
print(list(df.columns))
print("\nSample rows:")
print(df.head())
