from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def get_data():
    return send_from_directory("data", "high_temp_hotspots.geojson")

app.run(debug=True)
