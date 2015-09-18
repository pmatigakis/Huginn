import json

from flask import render_template, jsonify
import requests

from huginn.web import app

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/fdmdata")
def fdmdata():
    try:
        response = requests.get("http://%s:%d/fdmdata" % (app.config["FDM_HOST"], 
                                                          app.config["FDM_PORT"]))
    except requests.ConnectionError:
        print("Failed to get fdm data from simulator")
        return jsonify(result="error", cause="Connection error")
    
    response_data = json.loads(response.text)
    
    return jsonify(result="ok", fdm_data=response_data)
