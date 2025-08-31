import json
import math
import os

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

input_path = os.path.join('Data', 'Hospital_VIC.json')
output_path_200 = os.path.join('Data', 'Hospitals_200_Geelong.json')
output_path_100 = os.path.join('Data', 'Hospitals_100_Geelong.json')
center_lat = -38.1493
center_lon = 144.3598
radius_km_200 = 200
radius_km_100 = 100

with open(input_path, 'r') as infile:
    hospitals = json.load(infile)

within_200km = [
    h for h in hospitals
    if (
        'latitude' in h and 'longitude' in h and
        h['latitude'] is not None and h['longitude'] is not None and
        haversine(center_lat, center_lon, h['latitude'], h['longitude']) <= radius_km_200
    )
]

within_100km = [
    h for h in hospitals
    if (
        'latitude' in h and 'longitude' in h and
        h['latitude'] is not None and h['longitude'] is not None and
        haversine(center_lat, center_lon, h['latitude'], h['longitude']) <= radius_km_100
    )
]

with open(output_path_200, 'w') as outfile:
    json.dump(within_200km, outfile, indent=2)
with open(output_path_100, 'w') as outfile:
    json.dump(within_100km, outfile, indent=2)

print(f"Found {len(within_200km)} hospitals within 200km of Geelong.")
print(f"Found {len(within_100km)} hospitals within 100km of Geelong.")
