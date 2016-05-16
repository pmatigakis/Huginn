"""
The huginn_start script starts the simulator and the simulator server
"""

import logging
from argparse import ArgumentParser

from huginn import configuration
from huginn.simulator import SimulationBuilder
from huginn.validators import port_number, fdm_data_endpoint,\
                              is_valid_latitude, is_valid_longitude,\
                              is_valid_heading
from huginn.servers import SimulationServer

def get_arguments():
    parser = ArgumentParser(description="Huginn flight simulator")

    parser.add_argument("--web", action="store", type=port_number,
                        default=configuration.WEB_SERVER_PORT,
                        help="The web server port")

    parser.add_argument("--fdm",
                        action="append",
                        type=fdm_data_endpoint,
                        default=[],
                        help="The fdm data endpoint")

    parser.add_argument("--controls", action="store", type=port_number,
                        default=configuration.CONTROLS_PORT,
                        help="The controls port")

    parser.add_argument("--aircraft", action="store",
                        default=configuration.DEFAULT_AICRAFT,
                        choices=configuration.AVAILABLE_AIRCRAFT,
                        help="The aircraft model that will be used")

    parser.add_argument("--log_level", action="store",
                        choices=["critical", "error", "warning",
                                 "info", "debug"],
                        default="debug",
                        help="Enable debug logs")

    parser.add_argument("--dt", action="store", type=float,
                        default=configuration.DT,
                        help="the simulation timestep")

    parser.add_argument("--log", action="store", default=configuration.LOG_FILE,
                        help="The output log file")

    parser.add_argument("--trim", action="store_true",
                        help="trim the aircraft")

    parser.add_argument("--latitude", action="store", type=float,
                        default=configuration.LATITUDE,
                        help="The starting latitude")

    parser.add_argument("--longitude", action="store", type=float,
                        default=configuration.LONGITUDE,
                        help="The starting longitude")

    parser.add_argument("--altitude", action="store", type=float,
                        default=configuration.ALTITUDE,
                        help="The starting altitude")

    parser.add_argument("--airspeed", action="store", type=float,
                        default=configuration.AIRSPEED,
                        help="The starting airspeed")

    parser.add_argument("--heading", action="store", type=float,
                        default=configuration.HEADING,
                        help="The starting heading")

    return parser.parse_args()

def validate_arguments(args, logger):
    """Check if the script arguments have valid values

    Arguments:
    args: an ArgumentParser object
    logger: the Logger object that will record the error messages
    """
    if args.dt <= 0.0:
        logger.error("Invalid simulation timestep %f", args.dt)
        return False

    if args.airspeed < 0.0:
        logger.error("Invalid aircraft airspeed %f", args.airspeed)
        return False

    if not is_valid_latitude(args.latitude):
        logger.error("Invalid latitude %f", args.latitude)
        return False

    if not is_valid_longitude(args.longitude):
        logger.error("Invalid longitude %f", args.longitude)
        return False

    if not is_valid_heading(args.heading):
        logger.error("Invalid heading %f", args.heading)
        return False

    if args.altitude < 0.0:
        logger.error("Invalid altitude %f", args.altitude)
        return False

    return True

def initialize_logger(output_file, log_level):
    if log_level == "critical":
        logger_log_level = logging.CRITICAL
    elif log_level == "error":
        logger_log_level = logging.ERROR
    elif log_level == "warning":
        logger_log_level = logging.WARNING
    elif log_level == "info":
        logger_log_level = logging.INFO
    elif log_level == "debug":
        logger_log_level = logging.DEBUG
    else:
        print("Unknown log level %s" % log_level)
        exit(1)

    logger = logging.getLogger("huginn")
    logger.setLevel(logger_log_level)

    formater = logging.Formatter("%(asctime)s - %(module)s - %(levelname)s - %(message)s")

    file_logging_handler = logging.FileHandler(output_file)
    file_logging_handler.setLevel(logger_log_level)
    file_logging_handler.setFormatter(formater)

    console_logging_handler = logging.StreamHandler()
    console_logging_handler.setLevel(logger_log_level)
    console_logging_handler.setFormatter(formater)

    logger.addHandler(file_logging_handler)
    logger.addHandler(console_logging_handler)

    return logger

def main():
    args = get_arguments()

    logger = initialize_logger(args.log, args.log_level)

    logger.info("Starting the Huginn flight simulator")

    huginn_data_path = configuration.get_data_path()

    if not validate_arguments(args, logger):
        logger.error("Invalid simulator arguments")
        exit(1)

    simulator_builder = SimulationBuilder(huginn_data_path)
    simulator_builder.aircraft = args.aircraft
    simulator_builder.trim = args.trim
    simulator_builder.dt = args.dt

    simulator_builder.latitude = args.latitude
    simulator_builder.longitude = args.longitude
    simulator_builder.altitude = args.altitude
    simulator_builder.airspeed = args.airspeed
    simulator_builder.heading = args.heading

    logger.debug("Creating the simulator")
    simulator = simulator_builder.create_simulator()

    if not simulator:
        logger.error("Failed to create the simulator using the aircraft model '%s'", args.aircraft)
        exit(1)

    #start the simulator paused
    logger.debug("The simulator will start paused")
    simulator.pause()
    simulator.start_trimmed = args.trim

    logger.debug("creating the simulator server")
    simulator_server = SimulationServer(simulator)

    simulator_server.fdm_clients = args.fdm

    simulator_server.controls_port = args.controls

    simulator_server.web_server_port = args.web

    logger.debug("starting the simulator server")
    simulator_server.start()
