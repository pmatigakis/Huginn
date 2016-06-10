"""
This module contains classes that are used by Huginn's web server and web
clients
"""


import json

import requests
from twisted.internet import reactor
from autobahn.twisted.websocket import (WebSocketServerFactory,
                                        WebSocketServerProtocol)


class WebClient(object):
    """The WebClient is used to retrieve flight data from Huginn's web
    server"""
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def _get_json_data_from_endpoint(self, endpoint):
        """Get the data in json format"""
        url = "http://%s:%d/aircraft/%s" % (self.host, self.port, endpoint)

        response = requests.get(url)

        data = json.loads(response.text)

        return data

    def get_gps_data(self):
        """Get the gps data from the simulator and return them as a
        dictionary"""
        return self._get_json_data_from_endpoint("instruments/gps")

    def get_accelerometer_data(self):
        """Get the accelerometer data from the simulator and return them as a
        dictionary"""
        return self._get_json_data_from_endpoint("sensors/accelerometer")

    def get_gyroscope_data(self):
        """Get the gyroscope data from the simulator and return them as a
        dictionary"""
        return self._get_json_data_from_endpoint("sensors/gyroscope")

    def get_thermometer_data(self):
        """Get the temperature data from the simulator and return them as a
        dictionary"""
        return self._get_json_data_from_endpoint("sensors/thermometer")

    def get_pressure_sensor_data(self):
        """Get the atmospheric pressure data from the simulator and return
        them as a dictionary"""
        return self._get_json_data_from_endpoint("sensors/pressure_sensor")

    def get_pitot_tube_data(self):
        """Get the pitot tube data from the simulator and return them as a
        dictionary"""
        return self._get_json_data_from_endpoint("sensors/pitot_tube")

    def get_ins_data(self):
        """Get the inertial navigation system  data from the simulator and
        return them as a dictionary"""
        return self._get_json_data_from_endpoint("sensors/ins")

    def get_engine_data(self):
        """Get the engine data from the simulator and return them as a
        dictionary"""
        return self._get_json_data_from_endpoint("engine")

    def get_flight_controls(self):
        """Get the flight controls data from the simulator and return them as
        a dictionary"""
        return self._get_json_data_from_endpoint("controls")


class FDMDataWebSocketFactory(WebSocketServerFactory):
    """The FDMDataWebSocketFactory class is a factory that creates the
    protocol objects for the fdm data transmission through web sockets"""
    def __init__(self, fdm, update_rate, *args, **kwargs):
        WebSocketServerFactory.__init__(self, *args, **kwargs)

        self.fdm = fdm
        self.update_rate = update_rate


class FDMDataWebSocketProtocol(WebSocketServerProtocol):
    """The FDMDataWebSocketProtocol class if the protocol class that transmits
    the fdm data using a web socket"""
    def onConnect(self, request):
        reactor.callLater(1.0/self.factory.update_rate, self.send_fdm_data)

    def send_fdm_data(self):
        """Send the fdm data"""
        fdm_data = {
            "roll": self.factory.fdm.orientation.roll,
            "pitch": self.factory.fdm.orientation.pitch,
            "airspeed": self.factory.fdm.velocities.airspeed,
            "latitude": self.factory.fdm.position.latitude,
            "longitude": self.factory.fdm.position.longitude,
            "altitude": self.factory.fdm.position.altitude,
            "heading": self.factory.fdm.position.heading
        }

        payload = json.dumps(fdm_data).encode("utf8")

        self.sendMessage(payload, False)

        reactor.callLater(1.0/self.factory.update_rate, self.send_fdm_data)
