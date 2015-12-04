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
                        FDMData, AircraftIndex
from huginn.protocols import TelemetryFactory, ControlsProtocol, FDMDataProtocol

def initialize_web_server(simulator, aircraft, web_server_port):
    """Initialize the web server"""
    logging.debug("Starting web server at port %d", web_server_port)

    root = File(pkg_resources.resource_filename("huginn", "/static"))  # @UndefinedVariable

    aircraft_root = AircraftIndex()

    aircraft_root.putChild("gps", GPSData(aircraft))
    aircraft_root.putChild("accelerometer", AccelerometerData(aircraft))
    aircraft_root.putChild("gyroscope", GyroscopeData(aircraft))
    aircraft_root.putChild("thermometer", ThermometerData(aircraft))
    aircraft_root.putChild("pressure_sensor", PressureSensorData(aircraft))
    aircraft_root.putChild("pitot_tube", PitotTubeData(aircraft))
    aircraft_root.putChild("ins", InertialNavigationSystemData(aircraft))
    aircraft_root.putChild("engine", EngineData(aircraft))
    aircraft_root.putChild("flight_controls", FlightControlsData(aircraft))

    root.putChild("aircraft", aircraft_root)

    root.putChild("simulator", SimulatorControl(simulator))

    root.putChild("fdm", FDMData(aircraft))

    frontend = server.Site(root)

    reactor.listenTCP(web_server_port, frontend)  # @UndefinedVariable

def initialize_telemetry_server(aircraft, telemetry_port, telemetry_update_rate):
    """Initialize the telemetry server"""
    logging.debug("Starting telemetry server at port %d", telemetry_port)

    telemetry_factory = TelemetryFactory(aircraft)

    reactor.listenTCP(telemetry_port, telemetry_factory)  # @UndefinedVariable

    telemetry_updater = LoopingCall(telemetry_factory.update_clients)
    telemetry_updater.start(telemetry_update_rate)

def initialize_controls_server(aircraft, controls_port):
    """Initialize the controls server"""
    logging.debug("Starting aircraft controls server at port %d",
                 controls_port)

    controls_protocol = ControlsProtocol(aircraft)

    reactor.listenUDP(controls_port, controls_protocol)  # @UndefinedVariable

def initialize_fdm_data_server(aircraft, fdm_client_address, fdm_client_port, fdm_client_update_rate):
    """Initialize the fdm data server"""
    logging.debug("Sending fdm data to %s:%d" % (fdm_client_address, fdm_client_port))

    fdm_data_protocol = FDMDataProtocol(aircraft, fdm_client_address, fdm_client_port)

    reactor.listenUDP(0, fdm_data_protocol)  # @UndefinedVariable

    fdm_data_updater = LoopingCall(fdm_data_protocol.send_fdm_data)
    fdm_data_updater.start(fdm_client_update_rate)
