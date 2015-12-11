import logging
from argparse import ArgumentParser
import signal
import os

from twisted.internet.error import CannotListenError
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from huginn import configuration
from huginn.simulator import Simulator
from huginn.validators import port_number, fdm_data_endpoint, telemetry_endpoint
from huginn.fdm import create_aircraft_model, create_fdmexec
from huginn.network import initialize_controls_server, initialize_fdm_data_server,\
                           initialize_telemetry_server, initialize_web_server
from huginn.console import SimulatorStatePrinter

def get_arguments():
    parser = ArgumentParser(description="Huginn flight simulator")

    parser.add_argument("--dt", action="store", type=float, default=configuration.DT, help="The simulation timestep")
    
    parser.add_argument("--telemetry", 
                        action="store", 
                        type=telemetry_endpoint, 
                        default="%s,%f" % (configuration.TELEMETRY_PORT,
                                           configuration.TELEMETRY_DT),
                        help="The telemetry endpoint")
    
    parser.add_argument("--http", action="store", type=port_number, default=configuration.WEB_SERVER_PORT, help="The web server port")
    
    parser.add_argument("--fdm",
                        action="store",
                        type=fdm_data_endpoint,
                        default="%s,%d,%f" % (configuration.FDM_CLIENT_ADDRESS, configuration.FDM_CLIENT_PORT, configuration.FDM_CLIENT_DT), 
                        help="The fdm data endpoint")
    
    parser.add_argument("--controls", action="store", type=port_number, default=configuration.CONTROLS_PORT, help="The controls port")
    parser.add_argument("--aircraft", action="store", default="c172p", help="The aircraft model to use")
    parser.add_argument("--latitude", action="store", type=float, default=configuration.INITIAL_LATITUDE, help="The starting latitude")
    parser.add_argument("--longitude", action="store", type=float, default=configuration.INITIAL_LONGITUDE, help="The starting longitude")
    parser.add_argument("--altitude", action="store", type=float, required=True, help="The starting altitude")
    parser.add_argument("--airspeed", action="store", type=float, required=True, help="The starting airspeed")
    parser.add_argument("--heading", action="store", type=float, default=configuration.INITIAL_HEADING, help="The starting heading")

    return parser.parse_args()

def shutdown(self):
    logging.info("Shutting down the simulator")

    reactor.callFromThread(reactor.stop)  # @UndefinedVariable

def main():
    logging.basicConfig(format="%(asctime)s - %(module)s:%(levelname)s:%(message)s",
                        filename="huginn.log",
                        filemode="a",
                        level=logging.DEBUG)

    logging.info("Starting the Huginn flight simulator")

    jsbsim_path = os.environ.get("JSBSIM_HOME", None)

    if not jsbsim_path:
        logging.error("The environment variable JSBSIM_HOME doesn't exist")
        print("The environment variable JSBSIM_HOME doesn't exist")
        exit(-1)

    args = get_arguments() 

    fdmexec = create_fdmexec(jsbsim_path, args.dt)

    aircraft = create_aircraft_model(fdmexec, args.aircraft)

    if not aircraft:
        logging.error("Failed to create flight model with name %s using the aircraft %s", args.fdmmodel, args.aircraft)
        print("Failed to create flight model with name %s using the aircraft %s" % args.fdmmodel, args.aircraft)
        exit(-1)

    simulator = Simulator(fdmexec, aircraft)

    initial_conditions_valid = simulator.set_initial_conditions(args.latitude,
                                                                args.longitude,
                                                                args.altitude,
                                                                args.airspeed,
                                                                args.heading)

    if not initial_conditions_valid:
        logging.debug("Invalid Initial conditions: latitude=%f degrees, longitude=%f degrees, altitude=%f meters, airspeed=%f meters/second, heading=%f degrees",
                      args.latitude,
                      args.longitude,
                      args.altitude,
                      args.airspeed,
                      args.heading)
        print("Failed to set initial conditions")
        exit(-1)

    simulator_state_printer = SimulatorStatePrinter()
    simulator.add_simulator_event_listener(simulator_state_printer)

    reset_result = simulator.reset()

    if not reset_result:
        logging.error("Failed to reset the simulation")
        print("Failed to reset the simulation")
        exit(-1)

    fdm_client_address, fdm_client_port, fdm_client_update_rate = args.fdm 

    telemetry_port, telemetry_update_rate = args.telemetry

    try:
        initialize_fdm_data_server(aircraft, fdm_client_address, fdm_client_port, fdm_client_update_rate)
        initialize_controls_server(aircraft, args.controls)
        initialize_web_server(simulator, aircraft, args.http)
        initialize_telemetry_server(aircraft, telemetry_port, telemetry_update_rate)
    except CannotListenError as e:
        logging.error("Failed to listen on port %d", e.port)
        print("Failed to listen on port %d" % e.port)
        exit(-1)

    signal.signal(signal.SIGTERM, shutdown)

    fdm_updater = LoopingCall(simulator.run)
    fdm_updater.start(simulator.dt)

    logging.debug("Starting the event loop")
    reactor.run() # @UndefinedVariable
    logging.info("The simulator has shut down")

if __name__ == "__main__":
    main()
