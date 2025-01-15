from flask import Flask, request, render_template
import folium
from geopy.geocoders import Nominatim
import os

app = Flask(__name__)

def get_lat_lon(place_name):
    geolocator = Nominatim(user_agent="my_travel_map")
    location = geolocator.geocode(place_name)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate-map', methods=['POST'])
def generate_map():
    source = request.form['source']
    destination = request.form['destination']

    source_lat, source_lon = get_lat_lon(source)
    destination_lat, destination_lon = get_lat_lon(destination)

    if source_lat is None or destination_lat is None:
        return "Error: Could not find one or more locations. Please try again."

    my_map = folium.Map(location=[source_lat, source_lon], zoom_start=6)
    folium.Marker([source_lat, source_lon], popup="Source").add_to(my_map)
    folium.Marker([destination_lat, destination_lon], popup="Destination").add_to(my_map)
    my_map.save('templates/map.html')
    return render_template('map.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
app.run(debug=True, host='0.0.0.0', port=8000)

