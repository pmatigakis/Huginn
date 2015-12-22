#!/usr/bin/env python

import logging
from argparse import ArgumentParser
import inspect
from os import path

import huginn
from huginn import configuration
from huginn.simulator import Simulator
from huginn.validators import port_number, fdm_data_endpoint, telemetry_endpoint
from huginn.fdm import create_fdmexec
from huginn.aircraft import Aircraft
from huginn.servers import SimulationServer
from huginn.console import SimulatorStatePrinter

def get_arguments():
    parser = ArgumentParser(description="Huginn flight simulator")
    
    parser.add_argument("--telemetry", 
                        action="store", 
                        type=telemetry_endpoint, 
                        default="%s,%f" % (configuration.TELEMETRY_PORT,
                                           configuration.TELEMETRY_DT),
                        help="The telemetry endpoint")
    
    parser.add_argument("--web", action="store", type=port_number, default=configuration.WEB_SERVER_PORT, help="The web server port")
    
    parser.add_argument("--fdm",
                        action="store",
                        type=fdm_data_endpoint,
                        default="%s,%d,%f" % (configuration.FDM_CLIENT_ADDRESS, configuration.FDM_CLIENT_PORT, configuration.FDM_CLIENT_DT), 
                        help="The fdm data endpoint")
    
    parser.add_argument("--controls", action="store", type=port_number, default=configuration.CONTROLS_PORT, help="The controls port")
    parser.add_argument("--aircraft", action="store", default="Rascal", help="The aircraft model that will be used")

    return parser.parse_args()

def main():
    logging.basicConfig(format="%(asctime)s - %(module)s:%(levelname)s:%(message)s",
                        filename="huginn.log",
                        filemode="a",
                        level=logging.DEBUG)

    logging.info("Starting the Huginn flight simulator")

    args = get_arguments()

    #make sure the user is using a model we support
    if args.aircraft != "Rascal" and args.aircraft != "easystar":
        logging.error("%s is not a supported aircraft", args.aircraft)
        print("%s is not a supported aircraft" % args.aircraft)
        exit(-1)

    huginn_path = inspect.getfile(huginn)
    huginn_data_path = path.join(path.dirname(huginn_path), "data")

    fdmexec = create_fdmexec(huginn_data_path, args.aircraft, configuration.DT)

    if not fdmexec:
        logging.error("Failed to create flight model using the aircraft model '%s'", args.aircraft)
        print("Failed to create flight model using the aircraft model '%s'" % args.aircraft)
        exit(-1)

    aircraft = Aircraft(fdmexec)

    aircraft.run()

    logging.debug("Engine thrust after simulation start %f", aircraft.engine.thrust)

    simulator = Simulator(fdmexec, aircraft)

    simulator_state_printer = SimulatorStatePrinter()
    simulator.add_simulator_event_listener(simulator_state_printer)

    fdm_client_address, fdm_client_port, fdm_client_update_rate = args.fdm 

    telemetry_port, telemetry_update_rate = args.telemetry

    simulator_server = SimulationServer(simulator)

    simulator_server.fdm_client_address = fdm_client_address
    simulator_server.fdm_client_port = fdm_client_port
    simulator_server.fdm_client_update_rate = fdm_client_update_rate

    simulator_server.telemetry_port = telemetry_port
    simulator_server.telemetry_update_rate = telemetry_update_rate

    simulator_server.controls_port = args.controls
    
    simulator_server.web_server_port = args.web

    simulator_server.start()

if __name__ == "__main__":
    main()
