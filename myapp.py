from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>I changed this text to test something</h1><br>Congratulations! This is the flask webpage now."

@app.route("/map")
def map():
    start_coords = (-27.4705, 153.0260) ##Brisbane long/lat
    folium_map = folium.Map(location=start_coords, zoom_start=14)
    return folium_map._repr_html_()

if __name__ == "__main__":
    app.run()
