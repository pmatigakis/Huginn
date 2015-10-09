"""
This module contains classes that are used by Huginn's web server
"""

import json
import logging

from twisted.web.resource import Resource

class Index(Resource):
    isLeaf = False

    def __init__(self, fdmexec):
        Resource.__init__(self)

        self.fdmexec = fdmexec

    def getChild(self, name, request):
        if name == '':
            return self
        return Resource.getChild(self, name, request)

    def render_GET(self, request):
        return "Huginn is running"

class FlightDataResource(Resource):
    """This is the base class that can be used to create resource subclasses
    that return flight data"""
    def __init__(self, aircraft):
        Resource.__init__(self)
        self.aircraft = aircraft

    def get_flight_data(self):
        """This method must be overidden by the subclass. It should return a
        dictionary containing the requested flight data"""
        pass

    def render_GET(self, request):
        """Return the response with the flight data"""
        request.responseHeaders.addRawHeader("content-type", "application/json")

        flight_data = self.get_flight_data()

        return json.dumps(flight_data)

class GPSData(FlightDataResource):
    """This resource class will return the gps data in json format"""
    isLeaf = True

    def __init__(self, aircraft):
        FlightDataResource.__init__(self, aircraft)

    def get_flight_data(self):
        gps_data = {
            "latitude": self.aircraft.gps.latitude,
            "longitude": self.aircraft.gps.longitude,
            "altitude": self.aircraft.gps.altitude,
            "airspeed": self.aircraft.gps.airspeed,
            "heading": self.aircraft.gps.heading
        }

        return gps_data

class AccelerometerData(FlightDataResource):
    """This resource class will return the accelerometer data in json format"""
    isLeaf = True

    def __init__(self, aircraft):
        FlightDataResource.__init__(self, aircraft)

    def get_flight_data(self):
        accelerometer_data = {
            "x_acceleration": self.aircraft.accelerometer.x_acceleration,
            "y_acceleration": self.aircraft.accelerometer.y_acceleration,
            "z_acceleration": self.aircraft.accelerometer.z_acceleration
        }

        return accelerometer_data

class GyroscopeData(FlightDataResource):
    """This resource class will return the gyroscope data in json format"""
    isLeaf = True

    def __init__(self, aircraft):
        FlightDataResource.__init__(self, aircraft)

    def get_flight_data(self):
        gyroscope_data = {
            "roll_rate": self.aircraft.gyroscope.roll_rate,
            "pitch_rate": self.aircraft.gyroscope.pitch_rate,
            "yaw_rate": self.aircraft.gyroscope.yaw_rate,
        }

        return gyroscope_data

class ThermometerData(FlightDataResource):
    """This resource class will return the thermometer data in json format"""
    isLeaf = True

    def __init__(self, aircraft):
        FlightDataResource.__init__(self, aircraft)

    def get_flight_data(self):
        thermometer_data = {
            "temperature": self.aircraft.thermometer.temperature,
        }

        return thermometer_data

class PressureSensorData(FlightDataResource):
    """This resource class will return the pressure sensor data in json format"""
    isLeaf = True

    def __init__(self, aircraft):
        FlightDataResource.__init__(self, aircraft)

    def get_flight_data(self):
        pressure_sensor_data = {
            "static_pressure": self.aircraft.pressure_sensor.pressure,
        }

        return pressure_sensor_data

class PitotTubeData(FlightDataResource):
    """This resource class will return the pitot tube data in json format"""
    isLeaf = True

    def __init__(self, aircraft):
        FlightDataResource.__init__(self, aircraft)

    def get_flight_data(self):
        pitot_tube_data = {
            "dynamic_pressure": self.aircraft.pitot_tube.pressure,
        }

        return pitot_tube_data

class InertialNavigationSystemData(FlightDataResource):
    """This resource class will return the inertial navigation system data in
    json format"""
    isLeaf = True

    def __init__(self, aircraft):
        FlightDataResource.__init__(self, aircraft)

    def get_flight_data(self):
        inertial_navigation_system_data = {
            "latitude": self.aircraft.inertial_navigation_system.latitude,
            "longitude": self.aircraft.inertial_navigation_system.longitude,
            "altitude": self.aircraft.inertial_navigation_system.altitude,
            "airspeed": self.aircraft.inertial_navigation_system.airspeed,
            "heading": self.aircraft.inertial_navigation_system.heading,
            "roll": self.aircraft.inertial_navigation_system.roll,
            "pitch": self.aircraft.inertial_navigation_system.pitch,
        }

        return inertial_navigation_system_data

class EngineData(FlightDataResource):
    """This resource class will return the engine data in json format"""
    isLeaf = True

    def __init__(self, aircraft):
        FlightDataResource.__init__(self, aircraft)

    def get_flight_data(self):
        engine_data = {
            "engine_rpm": self.aircraft.engine.rpm,
            "engine_thrust": self.aircraft.engine.thrust,
            "engine_power": self.aircraft.engine.power,
        }

        return engine_data

class FlightControlsData(FlightDataResource):
    """This resource class will return the flight controls data in json format"""
    isLeaf = True

    def __init__(self, aircraft):
        FlightDataResource.__init__(self, aircraft)

    def get_flight_data(self):
        flight_controls_data = {
            "aileron": self.aircraft.controls.aileron,
            "elevator": self.aircraft.controls.elevator,
            "rudder": self.aircraft.controls.rudder,
            "throttle": self.aircraft.engine.throttle,
        }

        return flight_controls_data

class SimulatorControl(Resource):
    isLeaf = True

    def __init__(self, fdm_model):
        Resource.__init__(self)
        self.fdm_model = fdm_model

    def invalid_request(self, request):
        response_data = {"result": "error",
                         "reason": "invalid simulator command request"}

        return self.send_response(request, response_data)

    def invalid_command(self, request, command):
        response_data = {"result": "error",
                         "reason": "invalid simulator command",
                         "command": command}

        return self.send_response(request, response_data)

    def send_response(self, request, response_data):
        request.responseHeaders.addRawHeader("content-type", "application/json")

        return json.dumps(response_data)

    def render_POST(self, request):
        if not request.args.has_key("command"):
            logging.error("Invalid simulator control request")

            return self.invalid_request(request)

        simulator_command = request.args["command"][0]

        if simulator_command == "pause":
            logging.debug("Pausing the simulator")
            self.fdm_model.pause()
        elif simulator_command == "resume":
            logging.debug("Resuming simulation")
            self.fdm_model.resume()
        elif simulator_command == "reset":
            logging.debug("Reseting the simulator")
            self.fdm_model.reset()
        else:
            logging.error("Invalid simulator command %s", simulator_command)
            return self.invalid_command(request, simulator_command)

        response_data = {"command": simulator_command, "result": "ok"}

        return self.send_response(request, response_data)
