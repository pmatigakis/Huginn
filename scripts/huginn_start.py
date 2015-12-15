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
from huginn.fdm import create_fdmexec
from huginn.aircraft import Aircraft
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
    parser.add_argument("--script", action="store", default="/scripts/737_cruise.xml", help="The script to load")
    parser.add_argument("--jsbsim", action="store", required=False, help="The path to jsbsim source code")

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

    args = get_arguments()

    if args.jsbsim:
        jsbsim_path = args.jsbsim
    else:
        jsbsim_path = os.environ.get("JSBSIM_HOME", None)

        if not jsbsim_path:
            logging.error("The environment variable JSBSIM_HOME doesn't exist")
            print("The environment variable JSBSIM_HOME doesn't exist")
            exit(-1) 

    fdmexec = create_fdmexec(jsbsim_path, args.script, args.dt)

    if not fdmexec:
        logging.error("Failed to create flight model")
        print("Failed to create flight model")
        exit(-1)

    aircraft = Aircraft(fdmexec)

    simulator = Simulator(fdmexec, aircraft)

    simulator_state_printer = SimulatorStatePrinter()
    simulator.add_simulator_event_listener(simulator_state_printer)

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
