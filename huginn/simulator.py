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
from huginn.protocols import SensorDataProtocol, ControlsProtocol,\
                             TelemetryFactory, FDMDataProtocol

class Simulator(object):
    def __init__(self, fdm_model):
        self.fdm_model = fdm_model
        self.aircraft = Aircraft(fdm_model)

    def _update_fdm(self):
        #running = self.fdm_model.run()
        running = self.aircraft.run()

        if not running:
            logging.error("Failed to update the flight dynamics model")
            self.shutdown()

    def shutdown(self):
        logging.info("Shutting down the simulator")

        reactor.callFromThread(reactor.stop)  # @UndefinedVariable

    def add_sensors_server(self, sensors_server_port):
        logging.info("Adding a sensors server at port %d",
                     sensors_server_port)

        sensors_data_protocol = SensorDataProtocol(self.aircraft)

        reactor.listenUDP(sensors_server_port, sensors_data_protocol) # @UndefinedVariable

    def add_controls_server(self, controls_server_port):
        logging.info("Adding an aircraft controls server at port %d",
                     controls_server_port)

        controls_protocol = ControlsProtocol(self.aircraft)

        reactor.listenUDP(controls_server_port, controls_protocol) # @UndefinedVariable

    def add_telemetry_server(self, telemetry_port, dt):
        logging.info("Adding a telemetry server at port %d", telemetry_port)

        telemetry_factory = TelemetryFactory(self.fdm_model, self.aircraft)

        reactor.listenTCP(telemetry_port, telemetry_factory) # @UndefinedVariable

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

        reactor.listenTCP(http_port, frontend) # @UndefinedVariable

    def add_fdm_client(self, host, port, dt):
        fdm_data_protocol = FDMDataProtocol(self.fdm_model, self.aircraft, host, port)
                
        reactor.listenUDP(0, fdm_data_protocol) # @UndefinedVariable

        fdm_data_updater = LoopingCall(fdm_data_protocol.send_fdm_data) # @UndefinedVariable
        fdm_data_updater.start(dt)

    def run(self):
        logging.info("Starting the simulator")

        fdm_updater = LoopingCall(self._update_fdm)
        fdm_updater.start(self.fdm_model.dt)

        self.fdm_model.pause()

        logging.debug("Starting the event loop")
        reactor.run() # @UndefinedVariable
        logging.info("The simulator has shut down")

        return True

def create_simulation(fdm_model_creator):
    fdm_model = fdm_model_creator.create_fdm_model()

    if not fdm_model:
        return None

    return Simulator(fdm_model)
