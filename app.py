from flask import Flask, render_template, jsonify
import pandas as pd
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def load_population_data():
    data_url = os.getenv('POPULATION_DATA_URL', 'cleaned_data.csv')
    df = pd.read_csv(data_url)
    print("Population data loaded.")
    return df

def load_geojson_data():
    geojson_url = os.getenv('GEOJSON_DATA_URL', 'counties_data.json')
    if geojson_url.startswith('http'):
        import requests
        response = requests.get(geojson_url)
        print("GeoJSON loaded from web.")
        return response.json()
    else:
        with open(geojson_url, 'r') as f:
            print("GeoJSON loaded from file.")
            return json.load(f)

def get_map_data():
    """Combine population data with GeoJSON data for the map visualization."""
    # Load data
    df = load_population_data()
    geojson = load_geojson_data()
    
    # Create county population dictionary
    county_data = {
        row['county'].replace(' County', '').lower(): {
            'name': row['county'].replace(' County', ''),
            'population': int(row['2024'])
        }
        for _, row in df.iterrows()
    }
    
    # Add population data to GeoJSON properties
    for feature in geojson['features']:
        county_name = feature['properties']['name'].lower()
        if county_name in county_data:
            feature['properties'].update({
                'population': county_data[county_name]['population']
            })
    
    return geojson

@app.route('/')
def index():
    df = load_population_data()
    return render_template('index.html', data=df.to_dict('records'))

@app.route('/api/map-data')
def map_data():
    return jsonify(get_map_data())

if __name__ == '__main__':
    app.run(debug=True, port=5004)

