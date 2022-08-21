from flask import Flask, render_template
import folium

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/test")
def test():
    coords = (46, 142)
    map = folium.Map(location=coords, zoom_start=14)
    return render_template("test.html") + map._repr_html_()

if __name__ == "__main__":
    app.run()
