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

def initialize_web_server(simulator, aircraft, web_server_port):
    """Initialize the web server"""
    logging.info("Starting a web server at port %d", web_server_port)

    root = File(pkg_resources.resource_filename("huginn", "/static"))  # @UndefinedVariable

    root.putChild("gps", GPSData(aircraft))
    root.putChild("accelerometer", AccelerometerData(aircraft))
    root.putChild("gyroscope", GyroscopeData(aircraft))
    root.putChild("thermometer", ThermometerData(aircraft))
    root.putChild("pressure_sensor", PressureSensorData(aircraft))
    root.putChild("pitot_tube", PitotTubeData(aircraft))
    root.putChild("ins", InertialNavigationSystemData(aircraft))
    root.putChild("engine", EngineData(aircraft))
    root.putChild("flight_controls", FlightControlsData(aircraft))
    root.putChild("fdm", FDMData(aircraft))
    root.putChild("simulator", SimulatorControl(simulator))

    frontend = server.Site(root)

    reactor.listenTCP(web_server_port, frontend)  # @UndefinedVariable

def initialize_telemetry_server(aircraft, telemetry_port, telemetry_update_rate):
    """Initialize the telemetry server"""
    logging.info("Adding a telemetry server at port %d", telemetry_port)

    telemetry_factory = TelemetryFactory(aircraft)

    reactor.listenTCP(telemetry_port, telemetry_factory)  # @UndefinedVariable

    telemetry_updater = LoopingCall(telemetry_factory.update_clients)
    telemetry_updater.start(telemetry_update_rate)

def initialize_sensors_server(aircraft, sensors_port):
    """Initialize the sonsors server"""
    logging.info("Adding a sensors server at port %d",
                 sensors_port)

    sensors_data_protocol = SensorDataProtocol(aircraft)

    reactor.listenUDP(sensors_port, sensors_data_protocol)  # @UndefinedVariable

def initialize_controls_server(aircraft, controls_port):
    """Initialize the controls server"""
    logging.info("Adding an aircraft controls server at port %d",
                 controls_port)

    controls_protocol = ControlsProtocol(aircraft)

    reactor.listenUDP(controls_port, controls_protocol)  # @UndefinedVariable

def initialize_fdm_data_server(aircraft, fdm_client_address, fdm_client_port, fdm_client_update_rate):
    """Initialize the fdm data server"""
    fdm_data_protocol = FDMDataProtocol(aircraft, fdm_client_address, fdm_client_port)

    reactor.listenUDP(0, fdm_data_protocol)  # @UndefinedVariable

    fdm_data_updater = LoopingCall(fdm_data_protocol.send_fdm_data)
    fdm_data_updater.start(fdm_client_update_rate)
