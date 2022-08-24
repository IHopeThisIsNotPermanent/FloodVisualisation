from flask import Flask, render_template
import folium

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

@app.route("/test")
def test():
    map = make_map(None)
    return render_template("header.html") + render_template("test.html") + map._repr_html_()

@app.route("/test/<coords>")
def test_specific(coords):
    map = make_map(coords)
    return render_template("header.html") + render_template("test.html") + map._repr_html_()

def make_map(coords):
    if coords is None:
        coords = (-27.4705, 153.0260)
    else:
        coords = coords.split(",")
    map = folium.Map(location=coords, zoom_start=18)
    folium.Marker(location = coords, popup="Address", icon=folium.Icon(icon="glyphicon-flag")).add_to(map)
    map.add_child(folium.LatLngPopup()) #click map, marker pops up showing lat/lon
    return map

if __name__ == "__main__":
    app.run()
