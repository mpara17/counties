from flask import Flask, render_template, jsonify
import pandas as pd
import json

app = Flask(__name__)

def load_population_data():
    """Load and process population data from CSV file."""
    df = pd.read_csv('cleaned_data.csv')
    return df

def load_geojson_data():
    """Load GeoJSON data for Illinois counties."""
    with open('counties_data.json', 'r') as f:
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
            'population': int(row['2024']),
            'population_history': {
                year: int(row[year])
                for year in ['2020', '2021', '2022', '2023', '2024']
            }
        }
        for _, row in df.iterrows()
    }
    
    # Add population data to GeoJSON properties
    for feature in geojson['features']:
        county_name = feature['properties']['name'].lower()
        if county_name in county_data:
            feature['properties'].update({
                'population': county_data[county_name]['population'],
                'population_history': county_data[county_name]['population_history']
            })
    
    return geojson

@app.route('/')
def index():
    """Render the main page with population data table."""
    df = load_population_data()
    return render_template('index.html', data=df.to_dict('records'))

@app.route('/api/map-data')
def map_data():
    """API endpoint for map data."""
    return jsonify(get_map_data())

if __name__ == '__main__':
    app.run(debug=True, port=5004)
