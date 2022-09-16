from flask import Flask, render_template, request
import folium
from folium import GeoJson, plugins
from folium.plugins import HeatMap
import geopy
from geopy import Nominatim


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("header.html") + render_template("home.html")

@app.route("/calculator")
def calculator():
    return render_template("header.html") + render_template("calculator.html")

@app.route("/guide")
def guide():
    return render_template("header.html") + render_template("guide.html")

@app.route("/resources")
def resources():
    return render_template("header.html") + render_template("resources.html")

@app.route("/charts")
def charts():
    return render_template("header.html") + render_template("charts.html")

@app.route("/test", methods = ["POST", "GET"])
def test():
    """Address lookup"""
    locator = Nominatim(user_agent="addressLookup")
    if request.method == "POST":
        test = request.form["fname"]
        location = locator.geocode(test)
        ##location coords are location.longitude, location.latitude
        #TODO: only accept location within Wivenhoe region - need coords of contour region
        #if location not None: <- TODO: fix None exception
        try:
            return render_template("header.html") + render_template("contour.html", lat = location.latitude, long = location.longitude)
        except:
            return render_template("header.html") + render_template("calculator.html")
        #return f"<h1>{test}</h1><br><img src='https://cdn.britannica.com/44/4144-004-43DD2776/Peneus-setiferus.jpg'>"

    #default coords to 'brisbane' == Elizabeth St
    return render_template("header.html") + render_template("contour.html", lat = -27.4705, long = 153.0260 )

"""def make_map(coords):
    if coords is None:
        coords = (-27.4705, 153.0260)
    else:
        coords = coords.split(",")

    # Map
    map = folium.Map(location=coords, zoom_start=18)

    # Marker
    folium.Marker(location = coords, popup="Address", icon=folium.Icon(icon="glyphicon-flag")).add_to(map)
    map.add_child(folium.LatLngPopup()) #click map, marker pops up showing lat/lon

    # GeoJson
    text = ""
    with open("test.json", 'r') as f:
        text = f.read()
    GeoJson(text).add_to(map)

    # HeatMap
    heat_data = []
    for lat in range(0, 100):
        for long in range(0, 100):
            heat_data.append([float(lat), float(long), lat/10])
    HeatMap(heat_data).add_to(map)

    return map
"""
if __name__ == "__main__":
    app.run()
