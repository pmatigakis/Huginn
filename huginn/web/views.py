"""
The huginn.web.views module contains the views for the front-end
"""

from flask import render_template, abort, jsonify
import requests

from huginn.web import app

@app.route("/")
def flight_display():
    """Renders the prinamy flight display"""
    return render_template("flight_display.html")

@app.route("/flight_data")
def flight_data():
    """Renders a table with the flight data"""
    try:
        response = requests.get("http://%s:%d/fdm" % (app.config["huginn_host"], app.config["huginn_web_port"]))
    except requests.ConnectionError:
        return abort(500)

    return render_template("flight_data.html", data=response.json())

@app.route("/simulator/<command>")
def simulator_control(command):
    try:
        response = requests.post("http://%s:%d/simulator/%s" % (app.config["huginn_host"], app.config["huginn_web_port"], command))
        return jsonify(response.json())
    except requests.ConnectionError:
        return jsonify(result="error", command=command)
