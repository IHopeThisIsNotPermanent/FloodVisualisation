from geopy import Nominatim
from flask import render_template, url_for

def iframe_map(x, y):
    return url_for('_map', lat=x, long=y)

def address_lookup(term):
    locator = Nominatim(user_agent="addressLookup")
    result = locator.geocode(term)

    # Didn't find address
    if result is None:
        return render_template("header.html") + "<h1>Address lookup failed</h1>"

    # Found address
    (x,y) = (result.latitude, result.longitude)
    return render_template("header.html") + render_template("results.html", map_address=iframe_map(x, y))
