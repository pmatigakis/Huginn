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

def validate_initial_position(args):
    initial_position_valid = True

    if args.altitude <= 0.0:
        logging.error("The altitude must be greater than 0 feet")
        print("The altitude must be greater than 0 feet")
        initial_position_valid = False

    if args.heading < 0.0 or args.heading >= 360.0:
        logging.error("The heading must be between 0.0 and 360.0 degrees")
        print("The heading must be between 0.0 and 360.0 degrees")
        initial_position_valid = False

    if args.latitude < -90.0 or args.latitude > 90.0:
        logging.error("The latitude must be between -90.0 and 90.0 degrees")
        print("The latitude must be between -90.0 and 90.0 degrees")
        initial_position_valid = False

    if args.longitude < -180.0 or args.longitude > 180.0:
        logging.error("The longitude must be between -180.0 and 180.0 degrees")
        print("The longitude must be between -180.0 and 180.0 degrees")
        initial_position_valid = False

    return initial_position_valid

def validate_aircraft_initial_condition(args, aircraft):
    if not aircraft.trim_requirements.is_valid_altitude(args.altitude):
        logging.error("The given altitude was %f, The aircraft model requires an altitude between %f-%f meters",
                      args.altitude, aircraft.trim_requirements.min_altitude, aircraft.trim_requirements.max_altitude)

        print("The given altitude was %f, The aircraft model requires an altitude between %f-%f meters" % (
                      args.altitude,
                      aircraft.trim_requirements.min_altitude,
                      aircraft.trim_requirements.max_altitude)
        )

        return False

    if not aircraft.trim_requirements.is_valid_airspeed(args.airspeed):
        logging.error("The given airspeed was %f, The aircraft model requires an airspeed between %f-%f meters per second",
                      args.airspeed, aircraft.trim_requirements.min_airspeed, aircraft.trim_requirements.max_airspeed)

        print("The given airspeed was %f, The aircraft model requires an airspeed between %f-%f meters per second" % (
                      args.airspeed,
                      aircraft.trim_requirements.min_airspeed,
                      aircraft.trim_requirements.max_airspeed)
        )

        return False

    return True

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

    initial_condition_valid = validate_initial_position(args)
    
    if not initial_condition_valid:
        logging.error("Invalid initial position")
        exit(-1)

    fdmexec = create_fdmexec(jsbsim_path, args.dt)

    aircraft = create_aircraft_model(fdmexec, args.aircraft)

    if not aircraft:
        logging.error("Failed to create flight model with name %s using the aircraft %s", args.fdmmodel, args.aircraft)
        print("Failed to create flight model with name %s using the aircraft %s" % args.fdmmodel, args.aircraft)
        exit(-1)

    aircraft_initial_condition_valid = validate_aircraft_initial_condition(args, aircraft)

    if not aircraft_initial_condition_valid:
        logging.error("Invalid aircraft initial condition")
        exit(-1)

    simulator = Simulator(fdmexec, aircraft)

    simulator.set_initial_conditions(args.latitude,
                                     args.longitude,
                                     args.altitude,
                                     args.airspeed,
                                     args.heading)

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
