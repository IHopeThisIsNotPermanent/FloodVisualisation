from flask import Flask, render_template, request, url_for
import folium
from folium import GeoJson, plugins
from folium.plugins import HeatMap
import geopy
from functions import *

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

# Returns just a folium map HTML representation
# Called as an iframe most of the time
@app.route("/_map", methods=["GET"])
def _map():
    Lat = request.args.get('lat')
    Long = request.args.get('long')
    return render_template("contour.html", lat=Lat, long=Long)

@app.route("/charts")
def charts():
    return render_template("header.html") + render_template("charts.html")

@app.route("/manual", methods=["GET"])
def manual():
    # Has the same form for searching address if the user wants to try again
    # Explains the problem that occured (address not found or address out of bounds) ###Make that get sent
    # Otherwise gives a new form with lat/long boxes, tells the user to find and click on their address and copy the lat and long
    return manual_select_map(request.args.get('reason'))

@app.route("/results", methods = ["POST", "GET"])
def results():
    if request.method == "POST":
        try:
            return address_lookup(request.form["address"])
        except Exception:
            try:
                print(request.form["lat"])
                print(request.form["long"])
                return latlong_lookup(request.form["lat"], request.form["long"])
            except Exception:
                return redirect(url_for("home"))
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run()
