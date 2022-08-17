from flask import Flask

import folium

app = Flask(__name__)


@app.route('/')
def home():
    start_coords = (-27.4705, 153.0260) ##Brisbane long/lat
    folium_map = folium.Map(location=start_coords, zoom_start=14)
    return folium_map._repr_html_()


if __name__ == '__main__':
    app.run()
