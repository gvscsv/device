from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

# Firebase config
FIREBASE_URL = "https://waterdevice-ded68-default-rtdb.firebaseio.com/"
FIREBASE_SECRET = "OuWkw7XVxlxDJ5J0ySzmYCkGzgmKjbaCYzAiCIjK"

# Helper to read from Firebase
def firebase_get(path):
    url = f"{FIREBASE_URL}{path}.json?auth={FIREBASE_SECRET}"
    response = requests.get(url)
    return response.json()

# Helper to write to Firebase
def firebase_set(path, data):
    url = f"{FIREBASE_URL}{path}.json?auth={FIREBASE_SECRET}"
    response = requests.put(url, json=data)
    return response.ok

@app.route("/", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        relay_value = request.form.get("relay")
        firebase_set("control/relay", True if relay_value == "1" else False)

    flow_rate = firebase_get("sensor/flow_rate") or 0
    total_litres = firebase_get("sensor/total_litres") or 0
    relay = firebase_get("control/relay") or False

    return render_template("dashboard.html",
                           flow_rate=round(flow_rate, 2),
                           total_litres=round(total_litres, 2),
                           relay=relay)

if __name__ == "__main__":
    app.run(debug=True)
