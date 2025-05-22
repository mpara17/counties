import pandas as pd
import json
import requests

def create_geojson():
    # Read the CSV file
    df = pd.read_csv('cleaned_data.csv')
    
    # Download all US counties GeoJSON
    url = "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"
    response = requests.get(url)
    counties_geojson = response.json()
    
    # Filter for Illinois counties (STATE == '17')
    il_features = [f for f in counties_geojson['features'] if f['properties']['STATE'] == '17']
    
    # Create a mapping of county names to their geometries using 'NAME' property
    county_geometries = {}
    for feature in il_features:
        county_name = feature['properties']['NAME']
        county_geometries[county_name] = feature['geometry']
    
    # Create GeoJSON structure
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    
    # Add each county as a feature
    for _, row in df.iterrows():
        county_name = row['county'].replace(' County', '')
        if county_name in county_geometries:
            feature = {
                "type": "Feature",
                "properties": {
                    "name": row['county'],
                    "2020": int(row['2020']),
                    "2021": int(row['2021']),
                    "2022": int(row['2022']),
                    "2023": int(row['2023']),
                    "2024": int(row['2024'])
                },
                "geometry": county_geometries[county_name],
                "id": row['county']
            }
            geojson["features"].append(feature)
    
    # Save to JSON file
    with open('counties_data.json', 'w', encoding='utf-8') as f:
        json.dump(geojson, f, indent=2)

if __name__ == '__main__':
    create_geojson()
