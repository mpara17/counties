from flask import Flask, render_template, jsonify
import pandas as pd
import json

app = Flask(__name__)

def get_map_data():
    # Read the population data
    df = pd.read_csv('cleaned_data.csv')
    
    # Read GeoJSON data
    with open('counties_data.json', 'r') as f:
        geojson = json.load(f)
    
    # Create a dictionary of county populations
    county_data = {}
    for _, row in df.iterrows():
        county_name = row['county'].replace(' County', '')
        county_data[county_name.lower()] = {
            'name': county_name,
            'population': int(row['2024']),  # Using 2024 data
            'population_history': {
                '2020': int(row['2020']),
                '2021': int(row['2021']),
                '2022': int(row['2022']),
                '2023': int(row['2023']),
                '2024': int(row['2024'])
            }
        }
    
    # Add population data to GeoJSON properties
    for feature in geojson['features']:
        county_name = feature['properties']['name'].lower()
        if county_name in county_data:
            feature['properties']['population'] = county_data[county_name]['population']
            feature['properties']['population_history'] = county_data[county_name]['population_history']
    
    return geojson

@app.route('/')
def index():
    # Read the population data for the table
    df = pd.read_csv('cleaned_data.csv')
    data = df.to_dict('records')
    return render_template('index.html', data=data)

@app.route('/api/map-data')
def map_data():
    return jsonify(get_map_data())

if __name__ == '__main__':
    app.run(debug=True, port=5004)
