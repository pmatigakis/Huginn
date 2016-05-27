"""
The huginn.clients contains classes that can be used to communicate
and control huginn
"""


import csv
import json

import requests

from huginn import configuration


class MapClient(object):
    """The MapClient is used to load a weypoint file to the simulator so that
    waypoints can be seen on the web frontend"""
    def __init__(self,
                 host=configuration.WEB_SERVER_PORT,
                 port=configuration.WEB_SERVER_PORT):
        self.host = host
        self.port = port

    def load_from_csv(self, waypoint_file):
        """Load waypoints from a csv file. Every row must be in the following
        format

        waypoint_name,latitude,longitude
        """
        waypoints = []

        with open(waypoint_file, "r") as f:
            reader = csv.reader(f, delimiter=",")

            for row in reader:
                waypoint = {"name": row[0],
                            "latitude": float(row[1]),
                            'longitude': float(row[2])}

                waypoints.append(waypoint)

        response = requests.post("http://%s:%d/map" % (self.host, self.port),
                                 headers={'Content-Type': 'application/json'},
                                 json=waypoints)

        response = json.loads(response.text)

        if response["result"] != "ok":
            return False

        return True
