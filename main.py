from flask import Flask, jsonify
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/latest")
def return_latest_dust():
    return jsonify({
        "PM10": 10,
        "PM2.5": 10,
        "PM1": 10
    })
