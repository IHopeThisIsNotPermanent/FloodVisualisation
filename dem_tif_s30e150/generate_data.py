from Model import grid, linsample, get_quads
import numpy as np
import pandas as pd
import folium
import branca
from folium import plugins
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import geojsoncontour
import scipy as sp
import scipy.ndimage
import json
import os

LAT = [-27.3773, -27.5990]
LONG = [152.9029, 153.2002]

CONST = 1 / 1200

def years_to_weight(years):
    # 10, 20, 50, 100, 500
    # 1-0.8, 0.8-0.6, 0.6-0.4, 0.4-0.2, 0.2-0
    if years > 500:
        return 0
    return linsample([0,10,20,50,100,500],[1,0.8,0.6,0.4,0.2,0],[years, years, 1])[0]

"""
    make_contour_map(jsonFile):
        jsonFile: relative filename to JSON file containing [lat, long, risk] data
    Method adapted from github user tjansson60
    https://github.com/python-visualization/folium/issues/958#issuecomment-427156672
"""
def make_contour_map(jsonFile):
    # Variables to rewrite file for flask
    fileName = "../templates/contour.html"
    centerLine = '                    center: [{{lat}}, {{long}}],\n'
    centerLineIndex = 46
    iconLine = '                [{{lat}}, {{long}}],'
    iconLineIndex = 65

    # # Setup colourmap
    # For the contour function
    colours = ['turquoise', '#80FF00', 'yellow', '#FF5100', '#990202']
    vmin = 0
    vmax = 1
    # To make a legend on the map
    levels = len(colours)
    cm = branca.colormap.LinearColormap(colours, vmin=vmin, vmax=vmax).to_step(levels)

    # Read data from data file
    data = None
    with open(jsonFile, 'r') as f:
        data = json.loads(f.read())

    # Extract data into each column
    z = []
    y = []
    x = []

    for item in data:
        z.append(item[2])
        y.append(item[1])
        x.append(item[0])

    # Put data into dataframe from pandas
    df = pd.DataFrame({'latitude': x, 'longitude': y, 'risk': z})

    # Keep original data (needed for later)
    x_orig = np.asarray(df.longitude.tolist())
    y_orig = np.asarray(df.latitude.tolist())
    z_orig = np.asarray(df.risk.tolist())

    # Make a grid from the maximum and minimum (meshgrid makes 2D array)
    x_arr = np.linspace(np.min(x_orig), np.max(x_orig), 500)
    y_arr = np.linspace(np.min(y_orig), np.max(y_orig), 500)
    x_mesh, y_mesh = np.meshgrid(x_arr, y_arr)

    # Create a mesh based on the z (risk) values
    z_mesh = griddata((x_orig, y_orig), z_orig, (x_mesh, y_mesh), method='linear')

    # # Gaussian filter the grid to make it smoother
    # sigma = [0.25, 0.25]
    # z_mesh = sp.ndimage.gaussian_filter(z_mesh, sigma, mode='constant')

    # Create the contour
    contourf = plt.contourf(x_mesh, y_mesh, z_mesh, levels, colors=colours, linestyles='None', vmin=vmin, vmax=vmax)

    # Convert matplotlib contourf to geojson
    geojson = geojsoncontour.contourf_to_geojson(
        contourf=contourf,
        min_angle_deg=3.0,
        ndigits=5,
        stroke_width=1,
        fill_opacity=0.5)

    # Set up the folium plot
    # Origin doesn't matter because it gets replaced later on
    geomap = folium.Map([0, 0], zoom_start=18, tiles="cartodbpositron")

    folium.Marker(location = (0, 0), popup="Address", icon=folium.Icon(icon="glyphicon-flag")).add_to(geomap)
    # geomap.add_child(folium.LatLngPopup()) #click map, marker pops up showing lat/lon

    # Plot the contour plot on folium
    folium.GeoJson(
        geojson,
        style_function=lambda x: {
            'color': x['properties']['stroke'],
            'weight': x['properties']['stroke-width'],
            'fillColor': x['properties']['fill'],
            'opacity': 0.6,
        }).add_to(geomap)

    # Add the colormap to the folium map
    cm.caption = 'Risk'
    geomap.add_child(cm)

    # Save as static HTML file
    geomap.save(fileName)

    # Replace origin with variable which can be given by flask
    # First, get the file
    contents = []
    with open(fileName, "r") as f:
        contents = f.readlines()

    # Now change the desired line, and write to file again
    contents[centerLineIndex] = centerLine
    contents[iconLineIndex] = iconLine
    with open(fileName, "w") as f:
        f.writelines(contents)

if __name__ == "__main__":
    # Path check
    cwd = os.getcwd()
    if "/" in cwd:
        # Unix
        parent = cwd.split("/")[-1]
    else:
        # Windows
        parent = cwd.split("\\")[-1]
    if parent != "dem_tif_s30e150":
        print("This file must be run from the dem_tif_s30e150 folder")
        exit()

    lat = LAT[0]
    long = LONG[0]

    m = grid()
    a = []

    print("Querying model")

    while lat > LAT[1]:
        while long < LONG[1]:
            a.append([lat, long, years_to_weight(m.getfunc(long, lat)(1))])
            long += CONST
        long = LONG[0]
        lat -= CONST

    print(f"Generated {len(a)} points")
    print("Writing to data.txt")

    with open("../data.txt", "w") as f:
        f.write(json.dumps(a))

    print("Updating contour map with data.txt")
    make_contour_map("../data.txt")
    print("Done")
