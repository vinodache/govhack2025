import json
import os

def load_disadvantage_json(path):
    with open(path, 'r') as f:
        data = json.load(f)
    # Remove header/empty rows
    return [d for d in data if d.get('suburb_name') and d['suburb_name'] not in ('2021 Suburbs and Localities (SAL) Name', '')]

def update_geojson_with_disadvantage(geojson_path, disadvantage_path, output_path):
    with open(geojson_path, 'r') as f:
        geojson = json.load(f)
    disadvantage_data = load_disadvantage_json(disadvantage_path)
    # Build lookup by suburb name (case-insensitive, strip)
    disadv_lookup = {d['suburb_name'].strip().upper(): d for d in disadvantage_data}
    for feature in geojson['features']:
        props = feature.get('properties', {})
        loc_name = props.get('loc_name', '').strip().upper()
        disadv = disadv_lookup.get(loc_name)
        if disadv:
            props['Disadvantage_rank_VIC'] = disadv['Disadvantage_rank_VIC']
            props['Disadvantage_Score'] = disadv['Disadvantage_Score']
        else:
            props['Disadvantage_rank_VIC'] = None
            props['Disadvantage_Score'] = None
        feature['properties'] = props
    with open(output_path, 'w') as f:
        json.dump(geojson, f, indent=2)
    print(f"Updated {output_path} with disadvantage data.")

if __name__ == "__main__":
    update_geojson_with_disadvantage(
        geojson_path='suburbs_updated_with_dates_latest.geojson',
        disadvantage_path=os.path.join('Data', 'DisadvantageSuburbs_Victoria.json'),
        output_path='suburbs_updated_with_dates_latest_with_disadvantage.geojson'
    )
