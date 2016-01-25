#!/usr/bin/env python

import pkg_resources
import logging
from argparse import ArgumentParser

from huginn import configuration
from huginn.simulator import Simulator
from huginn.validators import port_number, fdm_data_endpoint
from huginn.fdm import FDMBuilder
from huginn.aircraft import Aircraft
from huginn.servers import SimulationServer
from huginn.console import SimulatorStatePrinter

def get_arguments():
    parser = ArgumentParser(description="Huginn flight simulator")
    
    parser.add_argument("--web", action="store", type=port_number, default=configuration.WEB_SERVER_PORT, help="The web server port")
    
    parser.add_argument("--fdm",
                        action="append",
                        type=fdm_data_endpoint,
                        default=[],
                        help="The fdm data endpoint")
    
    parser.add_argument("--controls", action="store", type=port_number, default=configuration.CONTROLS_PORT, help="The controls port")
    parser.add_argument("--aircraft", action="store", default="Rascal", help="The aircraft model that will be used")
    parser.add_argument("--debug", action="store_true", help="Enable debug logs")
    parser.add_argument("--dt", action="store", type=float, default=configuration.DT, help="the simulation timestep")
    parser.add_argument("--log", action="store", default="huginn.log", help="The output log file")
    parser.add_argument("--trim", action="store_true", help="trim the aircraft")
    
    parser.add_argument("--latitude", action="store", type=float, default=configuration.LATITUDE, help="The starting latitude")
    parser.add_argument("--longitude", action="store", type=float, default=configuration.LONGITUDE, help="The starting longitude")
    parser.add_argument("--altitude", action="store", type=float, default=configuration.ALTITUDE, help="The starting altitude")
    parser.add_argument("--airspeed", action="store", type=float, default=configuration.AIRSPEED, help="The starting airspeed")
    parser.add_argument("--heading", action="store", type=float, default=configuration.HEADING, help="The starting heading")

    return parser.parse_args()

def main():
    args = get_arguments()

    log_level = logging.INFO
    if args.debug:
        log_level = logging.DEBUG

    logger = logging.getLogger("huginn")
    logger.setLevel(log_level)

    formater = logging.Formatter("%(asctime)s - %(module)s - %(levelname)s - %(message)s")

    file_logging_handler = logging.FileHandler(args.log)
    file_logging_handler.setLevel(log_level)
    file_logging_handler.setFormatter(formater)

    console_logging_handler = logging.StreamHandler()
    console_logging_handler.setLevel(log_level)
    console_logging_handler.setFormatter(formater)

    logger.addHandler(file_logging_handler)
    logger.addHandler(console_logging_handler)

    logger.info("Starting the Huginn flight simulator")

    #make sure the user is using a model we support
    if args.aircraft != "Rascal" and args.aircraft != "easystar":
        logger.error("%s is not a supported aircraft", args.aircraft)
        exit(1)

    huginn_data_path = pkg_resources.resource_filename("huginn", "data")  # @UndefinedVariable

    if args.dt <= 0.0:
        logger.error("Invalid simulation timestep %f", args.dt)
        exit(1)

    fdm_builder = FDMBuilder(huginn_data_path)
    fdm_builder.aircraft = args.aircraft
    fdm_builder.trim = args.trim
    fdm_builder.dt = args.dt

    fdm_builder.latitude = args.latitude
    fdm_builder.longitude = args.longitude
    fdm_builder.altitude = args.altitude
    fdm_builder.airspeed = args.airspeed
    fdm_builder.heading = args.heading

    logger.debug("Creating the flight dynamics model")
    fdm = fdm_builder.create_fdm()

    if not fdm:
        logger.error("Failed to create flight model using the aircraft model '%s'", args.aircraft)
        exit(1)

    aircraft = Aircraft()
    fdm.update_aircraft(aircraft)

    logger.debug("Engine thrust after simulation start %f", aircraft.engine.thrust)

    simulator = Simulator(fdm, aircraft)
    #start the simulator paused
    logger.debug("The simulator will start paused")
    simulator.paused = True
    simulator.start_trimmed = args.trim

    simulator_state_printer = SimulatorStatePrinter()
    simulator.add_simulator_event_listener(simulator_state_printer)

    logger.debug("creating the simulator server")
    simulator_server = SimulationServer(simulator)

    simulator_server.fdm_clients = args.fdm

    simulator_server.controls_port = args.controls
    
    simulator_server.web_server_port = args.web

    logger.debug("starting the simulator server")
    simulator_server.start()

if __name__ == "__main__":
    main()
