import json
import os

# Input and output file paths
input_path = os.path.join('Data', 'Hospitals.json')
output_path = os.path.join('Data', 'Hospital_VIC.json')

def filter_vic_hospitals(input_path, output_path):
    with open(input_path, 'r') as infile:
        hospitals = json.load(infile)
    vic_hospitals = [h for h in hospitals if h.get('state') == 'Vic']
    with open(output_path, 'w') as outfile:
        json.dump(vic_hospitals, outfile, indent=2)
    print(f"Filtered {len(vic_hospitals)} VIC hospitals out of {len(hospitals)} total.")

if __name__ == "__main__":
    filter_vic_hospitals(input_path, output_path)
