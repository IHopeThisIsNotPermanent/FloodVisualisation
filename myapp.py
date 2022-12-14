from flask import Flask, render_template, request, url_for
import folium
from folium import GeoJson
import geopy
from functions import *

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("header.html") + render_template("index.html")

@app.route("/guide")
def guide():
    return render_template("header.html") + render_template("guide.html")

@app.route("/resources")
def resources():
    return render_template("header.html") + render_template("resources.html")

@app.route("/about")
def about():
    return render_template("header.html") + render_template("about.html")

# Returns just a folium map HTML representation
# Called as an iframe most of the time
@app.route("/_map", methods=["GET"])
def _map():
    Lat = request.args.get('lat')
    Long = request.args.get('long')
    return render_template("contour.html", lat=Lat, long=Long)

@app.route("/_man_map", methods=["GET"])
def _man_map():
    x1 = request.args.get('x1')
    x2 = request.args.get('x2')
    y1 = request.args.get('y1')
    y2 = request.args.get('y2')
    return render_template("manual_map.html", X1=x1, X2=x2, Y1=y1, Y2=y2)

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
                return latlong_lookup(request.form["lat"], request.form["long"])
            except Exception as e:
                print(e)
                return redirect(url_for("home"))
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run()
