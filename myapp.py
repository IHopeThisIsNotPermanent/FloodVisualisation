from flask import Flask, render_template, request
import folium
from folium import GeoJson, plugins
from folium.plugins import HeatMap
import logging

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("header.html") + render_template("index.html")

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
    if request.method == "POST" and request.form.get("zoom") != None:
        # Received a zoomend event from javascript
        logging.basicConfig(filename="zoom.txt",
                        filemode="a",
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)
        logging.info(f"Zoom level: {request.form.get('zoom')}")
        logger = logging.getLogger("zoom")
    elif request.method == "POST":
        test = request.form["fname"]
        return f"<h1>{test}</h1><br><img src='https://cdn.britannica.com/44/4144-004-43DD2776/Peneus-setiferus.jpg'>"
    map = make_map(None)

    #Saves map to a .html, for debugging purposes only
    map.save('foliummap.html')
    return render_template("header.html") + map._repr_html_() + render_template("test.html")

@app.route("/test/<coords>")
def test_specific(coords):
    map = make_map(coords)
    return render_template("header.html") + render_template("test.html") + map._repr_html_()

def make_map(coords):
    if coords is None:
        coords = (-27.4705, 153.0260)
    else:
        coords = coords.split(",")\

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
    
    # Get map's Javascript variable name
    map_js = map.get_name()

    # Renders html file so injected script appears at the end
    map.render()
    
    # Injects javascript
    map.get_root().script.add_child(folium.Element(f"""
    {map_js}.on("zoomend", function(){{
        console.log("User zoomed in or out. Zoom level: " + {map_js}.getZoom());
        console.log($(location).attr('href')); //in theory prints out url
        $.ajax({{
            type : 'POST',
            url : "http://localhost:5000/test", //replace with URL when deploying
            data : {{zoom: {map_js}.getZoom()}}
        }});
    }});
    """))

    return map

if __name__ == "__main__":
    app.run()
