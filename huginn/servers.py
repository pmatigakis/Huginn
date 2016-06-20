"""
The huginn.servers module contains classes that can be used to create
a simulator that transmits and receives data from/to the network
"""


import logging

from twisted.internet import reactor
from twisted.web import server
from twisted.internet.task import LoopingCall
from twisted.web.wsgi import WSGIResource
from flask import Flask, render_template
from flask_restful import Api

from huginn import configuration
from huginn.protocols import ControlsProtocol, FDMDataProtocol,\
                             SensorDataFactory
from huginn.http import FDMDataWebSocketFactory, FDMDataWebSocketProtocol
from huginn.rest import (FDMResource, AircraftResource, GPSResource,
                         AccelerometerResource, GyroscopeResource,
                         ThermometerResource, PressureSensorResource,
                         PitotTubeResource, InertialNavigationSystemResource,
                         EngineResource, FlightControlsResource,
                         SimulatorControlResource, AccelerationsResource,
                         VelocitiesResource, OrientationResource,
                         AtmosphereResource, ForcesResource,
                         InitialConditionResource, PositionResource)


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
        self.fdm_clients = []
        self.web_server_port = configuration.WEB_SERVER_PORT
        self.sensors_port = configuration.SENSORS_PORT
        self.websocket_port = configuration.WEBSOCKET_PORT
        self.websocket_update_rate = configuration.WEBSOCKET_UPDATE_RATE
        self.logger = logging.getLogger("huginn")

    def _initialize_controls_server(self):
        """Initialize the controls server"""
        self.logger.debug("Starting aircraft controls server at port %d",
                          self.controls_port)

        controls_protocol = ControlsProtocol(self.fdmexec)

        reactor.listenUDP(self.controls_port, controls_protocol)

    def _initialize_fdm_data_server(self):
        """Initialize the fdm data server"""
        for fdm_client in self.fdm_clients:
            client_address, client_port, dt = fdm_client
            self.logger.debug("Sending fdm data to %s:%d", client_address,
                              client_port)

            fdm_data_protocol = FDMDataProtocol(self.fdmexec,
                                                self.aircraft,
                                                client_address,
                                                client_port)

            reactor.listenUDP(0, fdm_data_protocol)

            fdm_data_updater = LoopingCall(fdm_data_protocol.send_fdm_data)
            fdm_data_updater.start(dt)

    def _run_simulator(self):
        result = self.simulator.run()

        if not result:
            self.logger.error("The simulator has failed to run")
            reactor.stop()

    def _initialize_simulator_updater(self):
        fdm_updater = LoopingCall(self._run_simulator)
        fdm_updater.start(self.dt)

    def _initialize_sensors_server(self):
        self.logger.debug("Starting the sensor server at port %d",
                          self.sensors_port)

        sensor_data_factory = SensorDataFactory(self.aircraft)

        reactor.listenTCP(self.sensors_port, sensor_data_factory)

    def _initialize_websocket_server(self):
        factory = FDMDataWebSocketFactory(
            self.simulator.fdm,
            self.websocket_update_rate,
            "ws://localhost:%d" % self.websocket_port
        )

        factory.protocol = FDMDataWebSocketProtocol

        reactor.listenTCP(self.websocket_port, factory)

    def _add_fdm_resources(self, api):
        api.add_resource(FDMResource, "/fdm",
                         resource_class_args=(self.fdmexec, self.aircraft))

        api.add_resource(AccelerationsResource, "/fdm/accelerations",
                         resource_class_args=(self.fdmexec,))

        api.add_resource(VelocitiesResource, "/fdm/velocities",
                         resource_class_args=(self.fdmexec,))

        api.add_resource(OrientationResource, "/fdm/orientation",
                         resource_class_args=(self.fdmexec,))

        api.add_resource(AtmosphereResource, "/fdm/atmosphere",
                         resource_class_args=(self.fdmexec,))

        api.add_resource(ForcesResource, "/fdm/forces",
                         resource_class_args=(self.fdmexec,))

        api.add_resource(InitialConditionResource, "/fdm/initial_condition",
                         resource_class_args=(self.fdmexec,))

        api.add_resource(PositionResource, "/fdm/position",
                         resource_class_args=(self.fdmexec,))

    def _initialize_web_frontend(self):
        app = Flask(__name__)

        api = Api()

        self._add_fdm_resources(api)

        api.add_resource(AircraftResource, "/aircraft",
                         resource_class_args=(self.aircraft,))

        api.add_resource(GPSResource, "/aircraft/instruments/gps",
                         resource_class_args=(self.aircraft.instruments.gps,))

        api.add_resource(
            AccelerometerResource,
            "/aircraft/sensors/accelerometer",
            resource_class_args=(self.aircraft.sensors.accelerometer,)
        )

        api.add_resource(
            GyroscopeResource,
            "/aircraft/sensors/gyroscope",
            resource_class_args=(self.aircraft.sensors.gyroscope,)
        )

        api.add_resource(
            ThermometerResource,
            "/aircraft/sensors/thermometer",
            resource_class_args=(self.aircraft.sensors.thermometer,)
        )

        api.add_resource(
            PressureSensorResource,
            "/aircraft/sensors/pressure_sensor",
            resource_class_args=(self.aircraft.sensors.pressure_sensor,)
        )

        api.add_resource(
            PitotTubeResource,
            "/aircraft/sensors/pitot_tube",
            resource_class_args=(self.aircraft.sensors.pitot_tube,)
        )

        api.add_resource(
            InertialNavigationSystemResource,
            "/aircraft/sensors/ins",
            resource_class_args=(
                self.aircraft.sensors.inertial_navigation_system,)
        )

        api.add_resource(
            EngineResource,
            "/aircraft/engine",
            resource_class_args=(self.aircraft.engine,)
        )

        api.add_resource(
            FlightControlsResource,
            "/aircraft/controls",
            resource_class_args=(self.aircraft.controls,)
        )

        api.add_resource(
            SimulatorControlResource,
            "/simulator",
            resource_class_args=(self.simulator,)
        )

        api.init_app(app)

        @app.route("/")
        def index():
            return render_template("index.html")

        resource = WSGIResource(reactor, reactor.getThreadPool(), app)
        site = server.Site(resource)

        reactor.listenTCP(self.web_server_port, site)

    def start(self):
        """Start the simulator server"""
        self._initialize_controls_server()
        self._initialize_fdm_data_server()
        self._initialize_sensors_server()
        self._initialize_simulator_updater()
        self._initialize_websocket_server()
        self._initialize_web_frontend()

        self.logger.info("Starting the simulator server")
        reactor.run()  # @UndefinedVariable
        self.logger.info("The simulator server has stopped")

    def stop(self):
        """Stop the simulator server"""
        self.logger.info("Shutting down the simulator server")
        reactor.stop()  # @UndefinedVariable
