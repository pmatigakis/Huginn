"""
The huginn.servers module contains classes that can be used to create
a simulator that transmits and receives data from/to the network
"""
import logging
import pkg_resources

from twisted.internet import reactor
from twisted.web import server
from twisted.web.static import File
from twisted.internet.task import LoopingCall

from huginn import configuration
from huginn.http import GPSData, AccelerometerData,\
                        GyroscopeData, ThermometerData, PressureSensorData,\
                        PitotTubeData, InertialNavigationSystemData,\
                        EngineData, FlightControlsData, SimulatorControl,\
                        FDMData, AircraftIndex, MapData
from huginn.protocols import TelemetryFactory, ControlsProtocol,\
                             FDMDataProtocol

class SimulationServer(object):
    """This class is the network front-end for the simulator. It will create
    and initialize the interfaces that can be used to control and receive
    simulation data."""
    def __init__(self, simulator):
        self.simulator = simulator
        self.fdmexec = simulator.fdmexec
        self.aircraft = simulator.aircraft
        self.dt = simulator.fdmexec.GetDeltaT()
        self.controls_port = configuration.CONTROLS_PORT
        self.fdm_client_address = configuration.FDM_CLIENT_ADDRESS
        self.fdm_client_port = configuration.FDM_CLIENT_PORT
        self.fdm_client_update_rate = configuration.FDM_CLIENT_DT
        self.web_server_port = configuration.WEB_SERVER_PORT
        self.telemetry_port = configuration.TELEMETRY_PORT
        self.telemetry_update_rate = configuration.TELEMETRY_DT
        self.logger = logging.getLogger("huginn")

    def _initialize_web_server(self):
        """Initialize the web server"""
        self.logger.debug("Starting web server at port %d", self.web_server_port)

        root = File(pkg_resources.resource_filename("huginn", "/static"))  # @UndefinedVariable

        aircraft_root = AircraftIndex()

        aircraft_root.putChild("gps", GPSData(self.aircraft))
        aircraft_root.putChild("accelerometer", AccelerometerData(self.aircraft))
        aircraft_root.putChild("gyroscope", GyroscopeData(self.aircraft))
        aircraft_root.putChild("thermometer", ThermometerData(self.aircraft))
        aircraft_root.putChild("pressure_sensor", PressureSensorData(self.aircraft))
        aircraft_root.putChild("pitot_tube", PitotTubeData(self.aircraft))
        aircraft_root.putChild("ins", InertialNavigationSystemData(self.aircraft))
        aircraft_root.putChild("engine", EngineData(self.aircraft))
        aircraft_root.putChild("flight_controls", FlightControlsData(self.aircraft))

        root.putChild("aircraft", aircraft_root)
        root.putChild("simulator", SimulatorControl(self.simulator))
        root.putChild("fdm", FDMData(self.aircraft))
        root.putChild("map", MapData())

        frontend = server.Site(root)

        reactor.listenTCP(self.web_server_port, frontend)  # @UndefinedVariable

    def _initialize_telemetry_server(self):
        """Initialize the telemetry server"""
        self.logger.debug("Starting telemetry server at port %d", self.telemetry_port)

        telemetry_factory = TelemetryFactory(self.aircraft)

        reactor.listenTCP(self.telemetry_port, telemetry_factory)  # @UndefinedVariable

        telemetry_updater = LoopingCall(telemetry_factory.update_clients)
        telemetry_updater.start(self.telemetry_update_rate)

    def _initialize_controls_server(self):
        """Initialize the controls server"""
        self.logger.debug("Starting aircraft controls server at port %d",
                     self.controls_port)

        controls_protocol = ControlsProtocol(self.aircraft)

        reactor.listenUDP(self.controls_port, controls_protocol)  # @UndefinedVariable

    def _initialize_fdm_data_server(self):
        """Initialize the fdm data server"""
        self.logger.debug("Sending fdm data to %s:%d", self.fdm_client_address, self.fdm_client_port)

        fdm_data_protocol = FDMDataProtocol(self.aircraft, self.fdm_client_address, self.fdm_client_port)

        reactor.listenUDP(0, fdm_data_protocol)  # @UndefinedVariable

        fdm_data_updater = LoopingCall(fdm_data_protocol.send_fdm_data)
        fdm_data_updater.start(self.fdm_client_update_rate)

    def _initialize_simulator_updater(self):
        fdm_updater = LoopingCall(self.simulator.run)
        fdm_updater.start(self.dt)

    def start(self):
        """Start the simulator server"""
        self._initialize_controls_server()
        self._initialize_fdm_data_server()
        self._initialize_telemetry_server()
        self._initialize_web_server()
        self._initialize_simulator_updater()

        self.logger.info("Starting the simulator server")
        reactor.run()  # @UndefinedVariable
        self.logger.info("The simulator server has stopped")

    def stop(self):
        """Stop the simulator server"""
        self.logger.info("Shutting down the simulator server")
        reactor.stop()  # @UndefinedVariable
