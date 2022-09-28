from geopy import Nominatim
from flask import render_template, url_for, redirect

def iframe_map(x, y):
    return url_for('_map', lat=x, long=y)

def address_lookup(term): # three arguments: term, lat, long, if term is none, use lat,long
    locator = Nominatim(user_agent="addressLookup")
    result = locator.geocode(term)

    # Didn't find address
    if result is None:
        # return render_template("header.html") + "<h1>Address lookup failed</h1>"
        # Go to manual location select page with reason 'failed'
        return redirect(url_for("/manual?reason=failed"))

    # Found address
    (x,y) = (result.latitude, result.longitude)
    # TODO: Check it is in bounds
    if False:
        return redirect(url_for("/manual?reason=bounds"))
    return render_template("header.html") + render_template("results.html", map_address=iframe_map(x, y))

def latlong_lookup(lat, long):
    try:
        lat = float(lat)
        long = float(long)
    except ValueError:
        # You have to be trolling to do this though...
        return redirect(url_for("/manual?reason=bounds"))
    return render_template("header.html") + render_template("results.html", map_address=iframe_map(lat, long))

def manual_select_map(reason):
    # Return map as ifram with bounding box of acceptable areas to click
    # On click: shows lat and long so that the user can copy
    if reason is None:
        return render_template("header.html") + render_template("manual.html")
    return render_template("header.html") + "<h1>In progress...</h1>"
