from geopy import Nominatim
from flask import render_template, url_for, redirect
from dem_tif_s30e150.Model import grid, linsample

import time

TL_BOUND = [-27.3773, 152.9029]
BR_BOUND = [-27.5990, 153.2002]

def iframe_map(x, y):
    return url_for('_map', lat=x, long=y)

def iframe_man_map():
    return url_for('_man_map', x1=TL_BOUND[1], x2=BR_BOUND[1], y1=TL_BOUND[0], y2=BR_BOUND[0])

def inbounds(x, y):
    if x <= TL_BOUND[0] and x >= BR_BOUND[0]:
        if y <= BR_BOUND[1] and y >= TL_BOUND[1]:
            return True
    return False

def address_lookup(term):
    locator = Nominatim(user_agent="addressLookup")
    result = locator.geocode(term)

    # Didn't find address
    if result is None:
        # Go to manual location select page with reason 'failed'
        return redirect(url_for("manual", reason="failed"))

    # Found address
    (x,y) = (result.latitude, result.longitude)

    # Check in bounds
    if not inbounds(x, y):
        return redirect(url_for("manual", reason="bounds"))

    # Render map at address
    return render_template("header.html") + render_template("results.html", map_address=iframe_map(x, y), tableData=generate_table(x,y), totalRisk=3.9)

def latlong_lookup(lat, long):
    # In case someone gets funny and puts non-floats into the coord boxes
    try:
        lat = float(lat)
        long = float(long)
        # Out of bounds
        if not inbounds(lat, long):
            return redirect(url_for("manual", reason="bounds"))
    except ValueError:
        # You have to be trolling to do this though...
        return redirect(url_for("manual", reason="bounds"))
    return render_template("header.html") + render_template("results.html", map_address=iframe_map(lat, long), tableData=generate_table(lat,long), totalRisk=3.9)

def manual_select_map(reason):
    # Normal page visitation
    if reason is None:
        reason = "none"
    elif reason not in ("bounds", "failed"):
        #Out of bounds, Address failed
        reason = "error, bad reason"
    #Debug text
    #f"<h1>{reason.capitalize()}</h1>" +

    return render_template("header.html") + render_template("manual.html", map_address=iframe_man_map(), reason=reason)

def generate_table(lat, long):
    out = []

    dat = grid()
    func = dat.getfunc(long, lat)
    sum = 0

    for i in [1, 2, 3, 4, 5, 10]:
        years = round(func(i))
        out.append(years)
        sum += years

    print(sum)

    try:
        out.append(round(linsample([6,60000,100000,300000,400000,599999],[10,8,6,4,2,0],[sum, sum, 1])[0], 2))
    except IndexError:
        out.append(0)

    print(out[-1])

    return out

if __name__ == "__main__":
    years = 1000
    print(round(linsample([6,60000,100000,300000,400000,500000],[10,8,6,4,2,0],[years, years, 1])[0], 2))
