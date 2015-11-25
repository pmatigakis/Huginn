"""
The huginn.network module contains classes that are used to provide an
interface to huginn via http or other network connections 
"""

import logging
import pkg_resources

from twisted.internet import reactor
from twisted.web import server
from twisted.web.static import File
from twisted.internet.task import LoopingCall

from huginn.http import GPSData, AccelerometerData,\
                        GyroscopeData, ThermometerData, PressureSensorData,\
                        PitotTubeData, InertialNavigationSystemData,\
                        EngineData, FlightControlsData, SimulatorControl,\
                        FDMData
from huginn.protocols import TelemetryFactory, SensorDataProtocol, ControlsProtocol, FDMDataProtocol

class WebServer(object):
    """The WebServer creates a web server that can be used to access flight
    data and control the simulator"""
    def __init__(self, simulator, aircraft, web_server_port):
        self.simulator = simulator
        self.aircraft = aircraft
        self.web_server_port = web_server_port

    def start(self):
        """Start the web server"""
        logging.info("Starting a web server at port %d", self.web_server_port)

        root = File(pkg_resources.resource_filename("huginn", "/static"))  # @UndefinedVariable

        root.putChild("gps", GPSData(self.aircraft))
        root.putChild("accelerometer", AccelerometerData(self.aircraft))
        root.putChild("gyroscope", GyroscopeData(self.aircraft))
        root.putChild("thermometer", ThermometerData(self.aircraft))
        root.putChild("pressure_sensor", PressureSensorData(self.aircraft))
        root.putChild("pitot_tube", PitotTubeData(self.aircraft))
        root.putChild("ins", InertialNavigationSystemData(self.aircraft))
        root.putChild("engine", EngineData(self.aircraft))
        root.putChild("flight_controls", FlightControlsData(self.aircraft))
        root.putChild("fdm", FDMData(self.aircraft))
        root.putChild("simulator", SimulatorControl(self.simulator))

        frontend = server.Site(root)

        reactor.listenTCP(self.web_server_port, frontend)  # @UndefinedVariable

class TelemetryServer(object):
    """The TelemetryServer transmits telemetry data on a tcp socket"""
    def __init__(self, aircraft, telemetry_port, telemetry_update_rate):
        self.aircraft = aircraft
        self.telemetry_port = telemetry_port
        self.telemetry_update_rate = telemetry_update_rate

    def start(self):
        """Start the telemetry server"""
        logging.info("Adding a telemetry server at port %d", self.telemetry_port)

        telemetry_factory = TelemetryFactory(self.aircraft)

        reactor.listenTCP(self.telemetry_port, telemetry_factory)  # @UndefinedVariable

        telemetry_updater = LoopingCall(telemetry_factory.update_clients)
        telemetry_updater.start(self.telemetry_update_rate)

class SensorsServer(object):
    def __init__(self, aircraft, sensors_port):
        self.aircraft = aircraft
        self.sensors_port = sensors_port

    def start(self):
        logging.info("Adding a sensors server at port %d",
                     self.sensors_port)

        sensors_data_protocol = SensorDataProtocol(self.aircraft)

        reactor.listenUDP(self.sensors_port, sensors_data_protocol)  # @UndefinedVariable

class ControlsServer(object):
    """The controls server if used to update the aircraft's control through a
    UDP socket"""
    def __init__(self, aircraft, controls_port):
        self.aircraft = aircraft
        self.controls_port = controls_port

    def start(self):
        """Start the controls server"""
        logging.info("Adding an aircraft controls server at port %d",
                     self.controls_port)

        controls_protocol = ControlsProtocol(self.aircraft)

        reactor.listenUDP(self.controls_port, controls_protocol)  # @UndefinedVariable

class FDMDataServer(object):
    """The FDMDataServer is used to transmit aircraft data through a UDP
    socket"""
    def __init__(self, aircraft, fdm_client_address, fdm_client_port, fdm_client_update_rate):
        self.aircraft = aircraft
        self.fdm_client_address = fdm_client_address
        self.fdm_client_port = fdm_client_port
        self.fdm_client_update_rate = fdm_client_update_rate

    def start(self):
        """Start teh fdm data server"""
        fdm_data_protocol = FDMDataProtocol(self.aircraft, self.fdm_client_address, self.fdm_client_port)

        reactor.listenUDP(0, fdm_data_protocol)  # @UndefinedVariable

        fdm_data_updater = LoopingCall(fdm_data_protocol.send_fdm_data)
        fdm_data_updater.start(self.fdm_client_update_rate)
