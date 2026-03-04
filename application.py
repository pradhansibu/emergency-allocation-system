from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import math

app = Flask(__name__)
application = app
socketio = SocketIO(app)

# Chandigarh Locations for 10 Ambulances
ambulances = [
    {"name": "Amb-Sector 17", "lat": 30.7421, "lon": 76.7827},
    {"name": "Amb-Sector 35", "lat": 30.7231, "lon": 76.7588},
    {"name": "Amb-PGI Hospital", "lat": 30.7651, "lon": 76.7744},
    {"name": "Amb-IT Park", "lat": 30.7180, "lon": 76.8120},
    {"name": "Amb-Manimajra", "lat": 30.7142, "lon": 76.8440},
    {"name": "Amb-Sector 43", "lat": 30.7130, "lon": 76.7400},
    {"name": "Amb-Sector 22", "lat": 30.7380, "lon": 76.7700},
    {"name": "Amb-Sector 15", "lat": 30.7550, "lon": 76.7700},
    {"name": "Amb-Mohali Border", "lat": 30.7050, "lon": 76.7200},
    {"name": "Amb-Sector 10", "lat": 30.7500, "lon": 76.7900}
]

def calculate_distance(lat1, lon1, lat2, lon2):
    # Mathematical Model for Research Paper
    R = 6371 # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('new_emergency')
def handle_emergency(data):
    e_lat, e_lon = data['lat'], data['lon']
    
    # Nearest Neighbor Algorithm Logic
    closest = min(ambulances, key=lambda x: calculate_distance(e_lat, e_lon, x['lat'], x['lon']))
    dist = calculate_distance(e_lat, e_lon, closest['lat'], closest['lon'])
    
    # Response Time (Avg Speed 40km/h)
    time_min = round((dist / 40) * 60, 2)
    
    emit('assign_ambulance', {
        'name': closest['name'],
        'distance': round(dist, 2),
        'time': time_min,
        'lat': closest['lat'],
        'lon': closest['lon']
    })

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000)
    socketio.run(app, debug=True)