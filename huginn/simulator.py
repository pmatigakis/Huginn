"""
The huginn.simulator module contains classes that are used to run an aircraft
simulation
"""

import logging

from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from twisted.web import server

from huginn.aircraft import Aircraft
from huginn.http import Index, GPSData, AccelerometerData,\
                        GyroscopeData, ThermometerData, PressureSensorData,\
                        PitotTubeData, InertialNavigationSystemData,\
                        EngineData, FlightControlsData, SimulatorControl
from huginn.protocols import FDMDataProtocol, ControlsProtocol,\
                             TelemetryFactory

class Simulator(object):
    def __init__(self, fdm_model):
        self.fdm_model = fdm_model
        self.aircraft = Aircraft(fdm_model)

    def _update_fdm(self):
        running = self.fdm_model.run()

        if not running:
            logging.error("Failed to update the flight dynamics model")
            self.shutdown()

    def shutdown(self):
        logging.info("Shutting down the simulator")

        reactor.callFromThread(reactor.stop)

    def add_fdm_server(self, fdm_server_port):
        logging.info("Adding a flight dynamics model server at port %d",
                     fdm_server_port)

        fdm_protocol = FDMDataProtocol(self.aircraft)

        reactor.listenUDP(fdm_server_port, fdm_protocol)

    def add_controls_server(self, controls_server_port):
        logging.info("Adding an aircraft controls server at port %d",
                     controls_server_port)

        controls_protocol = ControlsProtocol(self.aircraft)

        reactor.listenUDP(controls_server_port, controls_protocol)

    def add_telemetry_server(self, telemetry_port, dt):
        logging.info("Adding a telemetry server at port %d", telemetry_port)

        telemetry_factory = TelemetryFactory(self.fdm_model, self.aircraft)

        reactor.listenTCP(telemetry_port, telemetry_factory)

        telemetry_updater = LoopingCall(telemetry_factory.update_clients)
        telemetry_updater.start(dt)

    def add_web_server(self, http_port):
        logging.info("Starting a web server at port %d", http_port)

        index_page = Index(self.fdm_model)

        index_page.putChild("gps", GPSData(self.aircraft))
        index_page.putChild("accelerometer", AccelerometerData(self.aircraft))
        index_page.putChild("gyroscope", GyroscopeData(self.aircraft))
        index_page.putChild("thermometer", ThermometerData(self.aircraft))
        index_page.putChild("pressure_sensor", PressureSensorData(self.aircraft))
        index_page.putChild("pitot_tube", PitotTubeData(self.aircraft))
        index_page.putChild("ins", InertialNavigationSystemData(self.aircraft))
        index_page.putChild("engine", EngineData(self.aircraft))
        index_page.putChild("flight_controls", FlightControlsData(self.aircraft))
        index_page.putChild("simulator", SimulatorControl(self.fdm_model))

        frontend = server.Site(index_page)

        reactor.listenTCP(http_port, frontend)

    def run(self):
        logging.info("Starting the simulator")

        fdm_updater = LoopingCall(self._update_fdm)
        fdm_updater.start(self.fdm_model.dt())

        self.fdm_model.pause()

        logging.debug("Starting the event loop")
        reactor.run()
        logging.info("The simulator has shut down")

        return True

def create_simulation(fdm_model_creator):
    fdm_model = fdm_model_creator.create_fdm_model()

    if not fdm_model:
        return None

    return Simulator(fdm_model)
