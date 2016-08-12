"""
The huginn.clients contains classes that can be used to communicate
and control huginn
"""


import csv

import requests

from huginn import configuration


class MapClient(object):
    """The MapClient is used to load waypoints to the simulator"""
    def __init__(self,
                 host=configuration.WEB_SERVER_PORT,
                 port=configuration.WEB_SERVER_PORT):
        self.host = host
        self.port = port

    def load(self, waypoint_file):
        """Load waypoints from a csv file. Every row must be in the following
        format

        waypoint_name,latitude,longitude,altitude
        """
        waypoints = []

        with open(waypoint_file, "r") as f:
            reader = csv.reader(f, delimiter=",")

            for row in reader:
                waypoint = {"name": row[0],
                            "latitude": float(row[1]),
                            'longitude': float(row[2]),
                            "altitude": float(row[3])}

                waypoints.append(waypoint)

        for waypoint in waypoints:
            url = "http://{}:{}/map/waypoint/{}".format(
                self.host, self.port, waypoint["name"])

            response = requests.post(
                url,
                headers={'Content-Type': 'application/json'},
                json=waypoint
            )

            if response.status_code != 200:
                return None

        return waypoints

    def add_waypoint(self, name, latitude, longitude, altitude=0.0):
        """Add a waypoint

        Arguments:
        name: the waypoint's name
        latitude: the waypoint's latitude
        longitude: the waypoint's longitude
        altitude: the waypoint's altitude

        Returns a dictionary with the waypoint data
        """
        waypoint = {
            "latitude": latitude,
            "longitude": longitude,
            "altitude": altitude
        }

        url = "http://{}:{}/map/waypoint/{}".format(self.host, self.port, name)

        response = requests.post(url,
                                 headers={'Content-Type': 'application/json'},
                                 json=waypoint)

        if response.status_code != 200:
            return None

        return waypoint

    def delete_waypoint(self, name):
        """Delete a waypoint

        Arguments:
        name: the waypoint's altitude

        Returns a dictionary with the waypoint data
        """
        url = "http://{}:{}/map/waypoint/{}".format(self.host, self.port, name)

        response = requests.delete(url)

        if response.status_code != 200:
            return None

        return response.json()
