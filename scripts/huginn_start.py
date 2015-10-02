import os
import logging
from argparse import ArgumentParser
import signal

from twisted.internet import reactor, task
from twisted.web import server
from huginn_jsbsim import FGFDMExec

from huginn.protocols import FDMDataProtocol, ControlsProtocol,\
                             TelemetryFactory
from huginn.http import Index, GPSData, AccelerometerData,\
                        GyroscopeData, ThermometerData, PressureSensorData,\
                        PitotTubeData, InertialNavigationSystemData,\
                        EngineData, FlightControlsData, SimulatorControl
from huginn import configuration
from huginn.aircraft import Aircraft
from huginn.fdm import JSBSimFDMModel

def get_arguments():
    parser = ArgumentParser(description="Huginn flight simulator")

    parser.add_argument("--properties", action="store_true", help="Print the property catalog")
    parser.add_argument("--dt", action="store", default=configuration.DT, help="The simulation timestep")
    parser.add_argument("--telemetry", action="store", default=configuration.TELEMETRY_PORT, help="The telemetry port")
    parser.add_argument("--telemetry_dt", action="store", default=configuration.TELEMETRY_UPDATE_RATE, help="The telemetry update rate")
    parser.add_argument("--http", action="store", default=configuration.WEB_SERVER_PORT, help="The web server port")
    parser.add_argument("--fdm", action="store", default=configuration.FDM_PORT, help="The fdm data port")
    parser.add_argument("--controls", action="store", default=configuration.CONTROLS_PORT, help="The controls port")

    return parser.parse_args()

def create_fdm(dt, jsbsim_path):
    fdmexec = FGFDMExec()

    logging.debug("Using jsbsim data at %s", jsbsim_path)

    fdmexec.set_root_dir(jsbsim_path)
    fdmexec.set_aircraft_path("/aircraft")
    fdmexec.set_engine_path("/engine")
    fdmexec.set_systems_path("/systems")

    fdmexec.set_dt(dt)

    logging.debug("Will use aircraft %s with reset file %s",
                  configuration.AIRCRAFT_NAME,
                  configuration.RESET_FILE)

    fdmexec.load_model(configuration.AIRCRAFT_NAME)

    fdmexec.load_ic(configuration.RESET_FILE)

    logging.debug("Initial conditions: latitude=%f, longitude=%f, altitude=%f, airspeed=%f, heading=%f",
                  configuration.INITIAL_LATITUDE,
                  configuration.INITIAL_LONGITUDE,
                  configuration.INITIAL_ALTITUDE,
                  configuration.INITIAL_AIRSPEED,
                  configuration.INITIAL_HEADING)

    fdmexec.set_property_value("ic/lat-gc-deg", configuration.INITIAL_LATITUDE)
    fdmexec.set_property_value("ic/long-gc-deg", configuration.INITIAL_LONGITUDE)
    fdmexec.set_property_value("ic/h-sl-ft", configuration.INITIAL_ALTITUDE)
    fdmexec.set_property_value("ic/vt-kts", configuration.INITIAL_AIRSPEED)
    fdmexec.set_property_value("ic/psi-true-deg", configuration.INITIAL_HEADING)

    #the following statements will make the aircraft to start it's engine
    fdmexec.set_property_value("fcs/throttle-cmd-norm", 0.65)
    fdmexec.set_property_value("fcs/mixture-cmd-norm", 0.87)
    fdmexec.set_property_value("propulsion/magneto_cmd", 3.0)
    fdmexec.set_property_value("propulsion/starter_cmd", 1.0)

    initial_condition_result = fdmexec.run_ic()

    if not initial_condition_result:
        logging.error("Failed to set the flight dynamics model's initial condition")
        print("Failed to set the flight dynamics model's initial condition")
        exit(-1)

    running = fdmexec.run()

    if not running:
        logging.error("Failed to make initial flight dynamics model run")
        print("Failed to make initial flight dynamics model run")
        exit(-1)

    #run the simulation for some time before we attemt to trim the aircraft
    while running and fdmexec.get_sim_time() < 0.1:
        fdmexec.process_message()
        fdmexec.check_incremental_hold()

        running = fdmexec.run()

    #trim the aircraft
    result = fdmexec.trim()
    if not result:
        logging.error("Failed to trim the aircraft")
        print("Failed to trim the aircraft")
        exit(-1)

    return fdmexec

def init_web_server(args, fdm_model):    
    index_page = Index(fdm_model)
    aircraft = Aircraft(fdm_model)

    index_page.putChild("gps", GPSData(aircraft))
    index_page.putChild("accelerometer", AccelerometerData(aircraft))
    index_page.putChild("gyroscope", GyroscopeData(aircraft))
    index_page.putChild("thermometer", ThermometerData(aircraft))
    index_page.putChild("pressure_sensor", PressureSensorData(aircraft))
    index_page.putChild("pitot_tube", PitotTubeData(aircraft))
    index_page.putChild("ins", InertialNavigationSystemData(aircraft))
    index_page.putChild("engine", EngineData(aircraft))
    index_page.putChild("flight_controls", FlightControlsData(aircraft))
    index_page.putChild("simulator", SimulatorControl(fdm_model))

    http_port = args.http

    logging.info("Starting the web server at port %d", http_port)

    frontend = server.Site(index_page)
    reactor.listenTCP(http_port, frontend)

def init_fdm_server(args, fdm_model):
    aircraft = Aircraft(fdm_model)

    fdm_protocol = FDMDataProtocol(aircraft)
    fdm_port = args.fdm

    logging.info("Starting the flight dynamics model server at port %d", fdm_port)

    reactor.listenUDP(fdm_port, fdm_protocol)

    controls_protocol = ControlsProtocol(aircraft)
    controls_port = args.controls

    logging.info("Starting the aircraft controls server at port %d", controls_port)

    reactor.listenUDP(controls_port, controls_protocol)

def init_telemetry_server(args, fdm_model):
    aircraft = Aircraft(fdm_model)

    factory = TelemetryFactory(fdm_model, aircraft)
    
    reactor.listenTCP(args.telemetry, factory)
    
    return factory

def update_fdm(fdm_model):
    running = fdm_model.run()

    if not running:
        logging.error("Failed to update the flight dynamics model")
        print("Failed to update the flight dynamics model")
        shutdown()

def shutdown():
    logging.debug("Shutting down Huginn")

    reactor.callFromThread(reactor.stop)

def main():
    logging.basicConfig(format="%(asctime)s - %(module)s:%(levelname)s:%(message)s",
                        filename="huginn.log",
                        filemode="a",
                        level=logging.DEBUG)

    logging.info("Starting the Huginn flight simulator")

    args = get_arguments()

    dt = args.dt

    jsbsim_path = os.environ.get("JSBSIM_HOME", None)

    if not jsbsim_path:
        logging.error("The JSBSIM_HOME environment variable is not set")
        print("The JSBSIM_HOME environment variable is not set")
        exit(-1)

    fdmexec = create_fdm(dt, jsbsim_path)
    
    fdm_model = JSBSimFDMModel(fdmexec)

    init_fdm_server(args, fdm_model)
    init_web_server(args, fdm_model)
    factory = init_telemetry_server(args, fdm_model)

    fdm_updater = task.LoopingCall(update_fdm, fdm_model)
    fdm_updater.start(dt)

    telemetry_updater = task.LoopingCall(factory.update_clients)
    telemetry_updater.start(args.telemetry_dt)

    signal.signal(signal.SIGTERM, shutdown)

    fdmexec.hold()

    logging.debug("Starting the event loop")
    reactor.run()
    logging.info("The simulator has shut down")

if __name__ == "__main__":
    main()
