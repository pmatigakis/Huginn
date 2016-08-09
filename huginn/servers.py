"""
The huginn.servers module contains classes that can be used to create
a simulator that transmits and receives data from/to the network
"""


import logging

from twisted.web import server
from twisted.internet.task import LoopingCall
from twisted.web.wsgi import WSGIResource
from flask import Flask, render_template
from flask_restful import Api

from huginn.protocols import ControlsProtocol, SimulatorDataProtocol
from huginn.http import (SimulatorDataWebSocketFactory,
                         SimulatorDataWebSocketProtocol)

from huginn.rest import (FDMResource, AircraftResource, GPSResource,
                         AccelerometerResource, GyroscopeResource,
                         ThermometerResource, PressureSensorResource,
                         PitotTubeResource, InertialNavigationSystemResource,
                         EngineResource, FlightControlsResource,
                         SimulatorControlResource, AccelerationsResource,
                         VelocitiesResource, OrientationResource,
                         AtmosphereResource, ForcesResource,
                         InitialConditionResource, PositionResource,
                         AirspeedIndicatorResource, AltimeterResource,
                         AttitudeIndicatorResource, HeadingIndicatorResource,
                         VerticalSpeedIndicatorResource)


logger = logging.getLogger(__name__)


def initialize_controls_server(reactor, fdmexec, port):
    """Initialize the controls server

    Arguments:
    reactor: a Twisted reactor to use
    fdmexec: an JSBSim FGFDMExec object
    port: the ports to listen for the flight control data
    """
    logger.debug("Starting aircraft controls server at port %d", port)

    controls_protocol = ControlsProtocol(fdmexec)

    reactor.listenUDP(port, controls_protocol)


def initialize_simulator_data_server(reactor, simulator, clients):
    """Initialize the simulator data server

    Arguments:
    reactor: a Twisted reactor to use
    simulator: a Simulator object
    clients: a list of (address, port) tuples of the listening clients
    """
    for address, port, update_rate in clients:
        logger.debug("Sending fdm data to %s:%d every %f seconds",
                     address, port, update_rate)

        simulator_data_protocol = SimulatorDataProtocol(simulator,
                                                        address,
                                                        port)

        reactor.listenUDP(0, simulator_data_protocol)

        simulator_data_updater = LoopingCall(
            simulator_data_protocol.send_simulator_data)

        simulator_data_updater.start(update_rate)


def initialize_websocket_server(reactor, simulator, host, port):
    """Initialize the web socket server

    Arguments:
    reactor: a twisted reactor object
    simulator: an Simulator object
    host: the server host
    port: the port to listen to
    """
    logger.debug("The websocket interface runs on %s:%d", host, port)
    factory = SimulatorDataWebSocketFactory(
        simulator,
        "ws://%s:%d" % (host, port)
    )

    factory.protocol = SimulatorDataWebSocketProtocol

    reactor.listenTCP(port, factory)


def _add_fdm_resources(api, fdm, aircraft):
    api.add_resource(FDMResource, "/fdm",
                     resource_class_args=(fdm, aircraft))

    api.add_resource(AccelerationsResource, "/fdm/accelerations",
                     resource_class_args=(fdm.fdmexec,))

    api.add_resource(VelocitiesResource, "/fdm/velocities",
                     resource_class_args=(fdm.fdmexec,))

    api.add_resource(OrientationResource, "/fdm/orientation",
                     resource_class_args=(fdm.fdmexec,))

    api.add_resource(AtmosphereResource, "/fdm/atmosphere",
                     resource_class_args=(fdm.fdmexec,))

    api.add_resource(ForcesResource, "/fdm/forces",
                     resource_class_args=(fdm.fdmexec,))

    api.add_resource(InitialConditionResource, "/fdm/initial_condition",
                     resource_class_args=(fdm.fdmexec,))

    api.add_resource(PositionResource, "/fdm/position",
                     resource_class_args=(fdm.fdmexec,))


def _add_instrument_resources(api, instruments):
    api.add_resource(GPSResource, "/aircraft/instruments/gps",
                     resource_class_args=(instruments.gps,))

    api.add_resource(
        AirspeedIndicatorResource,
        "/aircraft/instruments/airspeed_indicator",
        resource_class_args=(instruments.airspeed_indicator,)
    )

    api.add_resource(
        AltimeterResource,
        "/aircraft/instruments/altimeter",
        resource_class_args=(instruments.altimeter,)
    )

    api.add_resource(
        AttitudeIndicatorResource,
        "/aircraft/instruments/attitude_indicator",
        resource_class_args=(instruments.attitude_indicator,)
    )

    api.add_resource(
        HeadingIndicatorResource,
        "/aircraft/instruments/heading_indicator",
        resource_class_args=(instruments.heading_indicator,)
    )

    api.add_resource(
        VerticalSpeedIndicatorResource,
        "/aircraft/instruments/vertical_speed_indicator",
        resource_class_args=(instruments.vertical_speed_indicator,)
    )


def _add_sensor_resources(api, sensors):
    api.add_resource(
        AccelerometerResource,
        "/aircraft/sensors/accelerometer",
        resource_class_args=(sensors.accelerometer,)
    )

    api.add_resource(
        GyroscopeResource,
        "/aircraft/sensors/gyroscope",
        resource_class_args=(sensors.gyroscope,)
    )

    api.add_resource(
        ThermometerResource,
        "/aircraft/sensors/thermometer",
        resource_class_args=(sensors.thermometer,)
    )

    api.add_resource(
        PressureSensorResource,
        "/aircraft/sensors/pressure_sensor",
        resource_class_args=(sensors.pressure_sensor,)
    )

    api.add_resource(
        PitotTubeResource,
        "/aircraft/sensors/pitot_tube",
        resource_class_args=(sensors.pitot_tube,)
    )

    api.add_resource(
        InertialNavigationSystemResource,
        "/aircraft/sensors/ins",
        resource_class_args=(sensors.inertial_navigation_system,)
    )


def initialize_web_server(reactor, simulator, port):
    """Initialize the web server

    :param reactor: the twisted reactor to use
    :param simulator: the Simulator ubject that will be used
    :param port: the port that the server will listen to
    """
    logger.debug("The web server will listen at port %d", port)

    app = Flask(__name__)

    api = Api()

    _add_fdm_resources(api, simulator.fdm, simulator.aircraft)

    _add_instrument_resources(api, simulator.aircraft.instruments)

    _add_sensor_resources(api, simulator.aircraft.sensors)

    api.add_resource(AircraftResource, "/aircraft",
                     resource_class_args=(simulator.aircraft,))

    api.add_resource(
        EngineResource,
        "/aircraft/engine",
        resource_class_args=(simulator.aircraft.engine,)
    )

    api.add_resource(
        FlightControlsResource,
        "/aircraft/controls",
        resource_class_args=(simulator.aircraft.controls,)
    )

    api.add_resource(
        SimulatorControlResource,
        "/simulator",
        resource_class_args=(simulator,)
    )

    api.init_app(app)

    @app.route("/")
    def index():
        return render_template("index.html")

    resource = WSGIResource(reactor, reactor.getThreadPool(), app)
    site = server.Site(resource)

    reactor.listenTCP(port, site)
