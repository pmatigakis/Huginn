"""
This module contains classes that are used by Huginn's web server and web
clients
"""
import json
import logging

import requests

from twisted.web.resource import Resource
from twisted.internet import reactor
from autobahn.twisted.websocket import (WebSocketServerFactory,
                                        WebSocketServerProtocol)

class AircraftResource(Resource):
    """This class serves as the root for the aircraft web resources."""
    isLeaf = False

    def __init__(self, aircraft):
        Resource.__init__(self)

        self.aircraft = aircraft

        self.putChild("sensors", SensorsResource(aircraft.sensors))
        self.putChild("instruments", InstrumentsResource(aircraft.instruments))
        self.putChild("engine", EngineData(self.aircraft.engine))

        self.putChild("flight_controls",
                      FlightControlsData(self.aircraft.controls))

    def getChild(self, name, request):
        if name == '':
            return self
        return Resource.getChild(self, name, request)

    def render_GET(self, request):
        request.responseHeaders.addRawHeader("content-type",
                                             "application/json")

        aircraft_info = {"aircraft_type": self.aircraft.type}

        return json.dumps(aircraft_info)

class SensorsResource(Resource):
    isLeaf = False

    def __init__(self, sensors):
        Resource.__init__(self)

        self.sensors = sensors

        self.putChild("accelerometer", AccelerometerData(sensors.accelerometer))
        self.putChild("gyroscope", GyroscopeData(sensors.gyroscope))
        self.putChild("thermometer", ThermometerData(sensors.thermometer))

        self.putChild("pressure_sensor",
                      PressureSensorData(sensors.pressure_sensor))

        self.putChild("pitot_tube", PitotTubeData(sensors.pitot_tube))
        self.putChild("ins", InertialNavigationSystemData(sensors.inertial_navigation_system))

    def getChild(self, name, request):
        if name == '':
            return self
        return Resource.getChild(self, name, request)

class InstrumentsResource(Resource):
    isLeaf = False

    def __init__(self, instruments):
        Resource.__init__(self)

        self.instruments = instruments

        self.putChild("gps", GPSData(instruments.gps))

    def getChild(self, name, request):
        if name == '':
            return self
        return Resource.getChild(self, name, request)

class FlightDataResource(Resource):
    """This is the base class that can be used to create resource subclasses
    that return flight data"""
    def __init__(self):
        Resource.__init__(self)

    def _get_flight_data(self):
        """This method must be overridden by the subclass. It should return a
        dictionary containing the requested flight data"""
        pass

    def render_GET(self, request):
        """Return the response with the flight data"""
        request.responseHeaders.addRawHeader("content-type",
                                             "application/json")

        flight_data = self._get_flight_data()

        return json.dumps(flight_data)

class GPSData(FlightDataResource):
    """This resource class will return the gps data in json format"""
    isLeaf = True

    def __init__(self, gps):
        FlightDataResource.__init__(self)
        self.gps = gps

    def _get_flight_data(self):
        gps_data = {
            "latitude": self.gps.latitude,
            "longitude": self.gps.longitude,
            "altitude": self.gps.altitude,
            "airspeed": self.gps.airspeed,
            "heading": self.gps.heading
        }

        return gps_data

class AccelerometerData(FlightDataResource):
    """This resource class will return the accelerometer data in json format"""
    isLeaf = True

    def __init__(self, accelerometer):
        FlightDataResource.__init__(self)

        self.accelerometer = accelerometer

    def _get_flight_data(self):
        accelerometer_data = {
            "x": self.accelerometer.x,
            "y": self.accelerometer.y,
            "z": self.accelerometer.z,
        }

        return accelerometer_data

class GyroscopeData(FlightDataResource):
    """This resource class will return the gyroscope data in json format"""
    isLeaf = True

    def __init__(self, gyroscope):
        FlightDataResource.__init__(self)

        self.gyroscope = gyroscope

    def _get_flight_data(self):
        gyroscope_data = {
            "roll_rate": self.gyroscope.roll_rate,
            "pitch_rate": self.gyroscope.pitch_rate,
            "yaw_rate": self.gyroscope.yaw_rate
        }

        return gyroscope_data

class ThermometerData(FlightDataResource):
    """This resource class will return the thermometer data in json format"""
    isLeaf = True

    def __init__(self, thermometer):
        FlightDataResource.__init__(self)

        self.thermometer = thermometer

    def _get_flight_data(self):
        thermometer_data = {
            "temperature": self.thermometer.temperature,
        }

        return thermometer_data

class PressureSensorData(FlightDataResource):
    """This resource class will return the pressure sensor data in json
    format"""
    isLeaf = True

    def __init__(self, pressure_sensor):
        FlightDataResource.__init__(self)

        self.pressure_sensor = pressure_sensor

    def _get_flight_data(self):
        pressure_sensor_data = {
            "static_pressure": self.pressure_sensor.pressure,
        }

        return pressure_sensor_data

class PitotTubeData(FlightDataResource):
    """This resource class will return the pitot tube data in json format"""
    isLeaf = True

    def __init__(self, pitot_tube):
        FlightDataResource.__init__(self)

        self.pitot_tube = pitot_tube

    def _get_flight_data(self):
        pitot_tube_data = {
            "total_pressure": self.pitot_tube.pressure,
        }

        return pitot_tube_data

class InertialNavigationSystemData(FlightDataResource):
    """This resource class will return the inertial navigation system data in
    json format"""
    isLeaf = True

    def __init__(self, inertial_navigation_system):
        FlightDataResource.__init__(self)

        self.inertial_navigation_system = inertial_navigation_system

    def _get_flight_data(self):
        inertial_navigation_system_data = {
            "latitude": self.inertial_navigation_system.latitude,
            "longitude": self.inertial_navigation_system.longitude,
            "altitude": self.inertial_navigation_system.altitude,
            "airspeed": self.inertial_navigation_system.airspeed,
            "heading": self.inertial_navigation_system.heading,
            "roll": self.inertial_navigation_system.roll,
            "pitch": self.inertial_navigation_system.pitch,
        }

        return inertial_navigation_system_data

class EngineData(FlightDataResource):
    """This resource class will return the engine data in json format"""
    isLeaf = True

    def __init__(self, engine):
        FlightDataResource.__init__(self)

        self.engine = engine

    def _get_flight_data(self):
        engine_data = {
            "thrust": self.engine.thrust,
            "throttle": self.engine.throttle,
        }

        return engine_data

class FlightControlsData(FlightDataResource):
    """This resource class will return the flight controls data in json
    format"""
    isLeaf = True

    def __init__(self, controls):
        FlightDataResource.__init__(self)

        self.controls = controls

    def _get_flight_data(self):
        flight_controls_data = {
            "aileron": self.controls.aileron,
            "elevator": self.controls.elevator,
            "rudder": self.controls.rudder,
            "throttle": self.controls.throttle,
        }

        return flight_controls_data

class FDMData(FlightDataResource):
    """The FDMData resource returns data relative to the simulation"""
    isLeaf = True
    def __init__(self, fdmexec, aircraft):
        FlightDataResource.__init__(self)
        self.fdmexec = fdmexec
        self.aircraft = aircraft

    def _get_flight_data(self):
        flight_data = {
            "time": self.fdmexec.GetSimTime(),
            "dt": self.fdmexec.GetDeltaT(),
            "latitude": self.aircraft.instruments.gps.latitude,
            "longitude": self.aircraft.instruments.gps.longitude,
            "altitude": self.aircraft.instruments.gps.altitude,
            "airspeed": self.aircraft.instruments.gps.airspeed,
            "heading": self.aircraft.instruments.gps.heading,
            "x_acceleration": self.aircraft.sensors.accelerometer.true_x,
            "y_acceleration": self.aircraft.sensors.accelerometer.true_y,
            "z_acceleration": self.aircraft.sensors.accelerometer.true_z,
            "roll_rate": self.aircraft.sensors.gyroscope.true_roll_rate,
            "pitch_rate": self.aircraft.sensors.gyroscope.true_pitch_rate,
            "yaw_rate": self.aircraft.sensors.gyroscope.true_yaw_rate,
            "temperature": self.aircraft.sensors.thermometer.true_temperature,
            "static_pressure": self.aircraft.sensors.pressure_sensor.true_pressure,
            "total_pressure": self.aircraft.sensors.pitot_tube.true_pressure,
            "roll": self.aircraft.sensors.inertial_navigation_system.true_roll,
            "pitch": self.aircraft.sensors.inertial_navigation_system.true_pitch,
            "thrust": self.aircraft.engine.thrust,
            "aileron": self.aircraft.controls.aileron,
            "elevator": self.aircraft.controls.elevator,
            "rudder": self.aircraft.controls.rudder,
            "throttle": self.aircraft.engine.throttle,
        }

        return flight_data

class SimulatorCommand(Resource):
    """The SimulatorCommand is the base class for the simulator commands that
    are called throught an http connection"""
    def __init__(self):
        Resource.__init__(self)

    def send_response(self, request, response_data):
        """Return the response in json format"""
        request.responseHeaders.addRawHeader("content-type",
                                             "application/json")

        return json.dumps(response_data)

class PauseSimulatorCommand(SimulatorCommand):
    """The PauseSimulatorCommand http command pauses the simulator"""
    isLeaf = True

    def __init__(self, simulator):
        SimulatorCommand.__init__(self)
        self.simulator = simulator
        self.logger = logging.getLogger("huginn")

    def render_POST(self, request):
        """Execute the command"""
        self.logger.debug("Pausing the simulator")
        self.simulator.pause()

        return self.send_response(request,
                                  {"command": "pause",
                                   "result": "ok"})

class ResumeSimulatorCommand(SimulatorCommand):
    """The PauseSimulatorCommand http command resumes the simulation"""
    isLeaf = True

    def __init__(self, simulator):
        SimulatorCommand.__init__(self)
        self.simulator = simulator
        self.logger = logging.getLogger("huginn")

    def render_POST(self, request):
        """Execute the command"""
        self.logger.debug("Resuming the simulator")
        self.simulator.resume()

        return self.send_response(request,
                                  {"command": "resume",
                                   "result": "ok"})

class ResetSimulatorCommand(SimulatorCommand):
    """The ResetSimulatorCommand http command resets the simulator"""
    isLeaf = True

    def __init__(self, simulator):
        SimulatorCommand.__init__(self)
        self.simulator = simulator
        self.logger = logging.getLogger("huginn")

    def render_POST(self, request):
        """Execute the command"""
        self.logger.debug("Reseting the simulator")

        reset_result = self.simulator.reset()
        if not reset_result:
            self.logger.error("Failed to reset the simulator")
            reactor.stop()  # @UndefinedVariable
            return self.send_response(request,
                                      {"command": "reset",
                                       "result": "error"})

        self.logger.debug("Pausing the simulator")
        self.simulator.pause()

        return self.send_response(request,
                                  {"command": "reset",
                                   "result": "ok"})

class StepSimulatorCommand(SimulatorCommand):
    """The StepSimulatorCommand http command executes a single simulation
    timestep"""
    isLeaf = True

    def __init__(self, simulator):
        SimulatorCommand.__init__(self)
        self.simulator = simulator
        self.logger = logging.getLogger("huginn")

    def render_POST(self, request):
        """Execute the command"""
        self.logger.debug("Executing a single simulation step")

        result = self.simulator.step()

        if not result:
            self.logger.error("The simulator has failed to run")
            reactor.stop()  # @UndefinedVariable
            return self.send_response(request,
                                      {"command": "step",
                                       "result": "error"})

        return self.send_response(request,
                                  {"command": "step",
                                   "result": "ok"})

class RunForSimulatorCommand(SimulatorCommand):
    """The RunForSimulatorCommand http command makes the simulator run for
    the given amount of time"""
    isLeaf = True

    def __init__(self, simulator):
        SimulatorCommand.__init__(self)
        self.simulator = simulator
        self.logger = logging.getLogger("huginn")

    def render_POST(self, request):
        """Execute the command"""
        time_to_run = float(request.args["time_to_run"][0])
        self.logger.debug("Running the simulation for %f seconds", time_to_run)

        result = self.simulator.run_for(time_to_run)

        if not result:
            self.logger.error("The simulator has failed to run for %f",
                              time_to_run)

            reactor.stop()  # @UndefinedVariable
            return self.send_response(request,
                                      {"command": "run_for",
                                       "result": "error"})

        return self.send_response(request,
                                  {"command": "run_for",
                                   "result": "ok"})

class SimulatorControl(Resource):
    """The SimulatorControl resource is used to control the simulator.
    For the moment it is possible to pause, resume, reset, run a
    single time step and run the simulation for a specified time"""
    isLeaf = False

    def __init__(self, simulator):
        Resource.__init__(self)
        self.simulator = simulator
        self.logger = logging.getLogger("huginn")
        self.putChild("reset", ResetSimulatorCommand(simulator))
        self.putChild("pause", PauseSimulatorCommand(simulator))
        self.putChild("resume", ResumeSimulatorCommand(simulator))
        self.putChild("step", StepSimulatorCommand(simulator))
        self.putChild("run_for", RunForSimulatorCommand(simulator))

    def getChild(self, name, request):
        if name == '':
            return self
        return Resource.getChild(self, name, request)

    def send_response(self, request, response_data):
        request.responseHeaders.addRawHeader("content-type",
                                             "application/json")

        return json.dumps(response_data)

    def render_GET(self, request):
        """The GET http method simply returns the state of the simulator in
        json format"""
        simulator_state = {
            "time": self.simulator.simulation_time,
            "dt": self.simulator.dt,
            "running": not self.simulator.is_paused()
        }

        return self.send_response(request, simulator_state)

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
        return self._get_json_data_from_endpoint("flight_controls")

class MapData(Resource):
    """The MapData resource returns the waypoints stored in the simulation
    server"""
    def __init__(self):
        Resource.__init__(self)
        self.waypoints = []

    def render_GET(self, request):
        request.responseHeaders.addRawHeader("content-type",
                                             "application/json")

        return json.dumps(self.waypoints)

    def render_POST(self, request):
        self.waypoints = json.loads(request.content.getvalue())

        request.responseHeaders.addRawHeader("content-type",
                                             "application/json")

        return json.dumps({"result": "ok"})

class FDMDataWebSocketFactory(WebSocketServerFactory):
    """The FDMDataWebSocketFactory class is a factory that creates the protocol
    objects for the fdm data transmission through web sockets"""
    def __init__(self, fdm, update_rate, *args, **kwargs):
        WebSocketServerFactory.__init__(self, *args, **kwargs)

        self.fdm = fdm
        self.update_rate = update_rate

class FDMDataWebSocketProtocol(WebSocketServerProtocol):
    """The FDMDataWebSocketProtocol class if the protocol class that transmits
    the fdm data using a web socket"""
    def onConnect(self, request):
        reactor.callLater(1.0/self.factory.update_rate, self.send_fdm_data)  # @UndefinedVariable

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

        reactor.callLater(1.0/self.factory.update_rate, self.send_fdm_data)  # @UndefinedVariable
