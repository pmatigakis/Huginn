"""
This module contains the views used by the front-end
"""
import json

from flask import render_template, jsonify
import requests

def index():
    """This is the index page view. It simply returns the page with the primary
    flight data display and the map."""
    return render_template("index.html")

class FlightDataView(object):
    def __init__(self, fdm_host, fdm_port):
        self.fdm_host = fdm_host
        self.fdm_port = fdm_port

    def __call__(self):
        """This is a view that returns the flight data that will be displayed
        by the primary flight display and the map widget."""
        try:
            response = requests.get("http://%s:%d/ins" % (self.fdm_host,
                                                          self.fdm_port))
        except requests.ConnectionError:
            print("Failed to get fdm data from simulator")
            return jsonify(result="error", cause="Connection error")

        response_data = json.loads(response.text)

        return jsonify(result="ok", fdm_data=response_data)
