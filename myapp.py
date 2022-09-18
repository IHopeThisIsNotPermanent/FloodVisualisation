from flask import Flask, render_template, request, url_for
import folium
from folium import GeoJson, plugins
from folium.plugins import HeatMap
import geopy
from geopy import Nominatim

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

@app.route("/_map", methods=["GET"])
def _map():
    Lat = request.args.get('lat')
    Long = request.args.get('long')
    return render_template("contour.html", lat=Lat, long=Long)

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
    # return render_template("header.html") + '<div>' + render_template("contour.html", lat = -27.4705, long = 153.0260 ) + "</div>"
    return render_template("header.html") + render_template("results.html", map_address=iframe_map(-27.4705, 153.0260))

def iframe_map(x, y):
    return url_for('_map', lat=x, long=y)

if __name__ == "__main__":
    app.run()
