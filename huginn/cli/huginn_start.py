"""
The huginn_start script starts the simulator and the simulator server
"""


import logging
from argparse import ArgumentParser

from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from huginn import configuration
from huginn.simulator import SimulationBuilder

from huginn.servers import (initialize_controls_server,
                            initialize_simulator_data_server,
                            initialize_websocket_server,
                            initialize_web_server)

from huginn.fdm import (TRIM_MODE_FULL, TRIM_MODE_GROUND,
                        TRIM_MODE_LONGITUDINAL, TRIM_MODE_PULLUP,
                        TRIM_MODE_TURN)

from huginn.cli import argtypes

TRIM_MODES = {
    "longitudinal": TRIM_MODE_LONGITUDINAL,
    "full": TRIM_MODE_FULL,
    "ground": TRIM_MODE_GROUND,
    "pullup": TRIM_MODE_PULLUP,
    # custom trim will not be supported by the simulator
    # "custom": 4,
    "turn": TRIM_MODE_TURN
}


def get_arguments():
    parser = ArgumentParser(description="Huginn flight simulator")

    parser.add_argument("--web", action="store", type=argtypes.port_number,
                        default=configuration.WEB_SERVER_PORT,
                        help="The web server port")

    parser.add_argument("--fdm",
                        action="append",
                        type=argtypes.fdm_data_endpoint,
                        default=[],
                        help="The fdm data endpoint")

    parser.add_argument("--controls", action="store",
                        type=argtypes.port_number,
                        default=configuration.CONTROLS_PORT,
                        help="The controls port")

    parser.add_argument("--debug", action="store_true",
                        help="Enable debug logs")

    parser.add_argument("--dt", action="store", type=argtypes.update_rate,
                        default=configuration.DT,
                        help="the simulation timestep")

    parser.add_argument("--log", action="store",
                        help="The output log file")

    parser.add_argument("--trim", action="store", choices=TRIM_MODES.keys(),
                        default="full", help="trim the aircraft")

    parser.add_argument("--latitude", action="store", type=argtypes.latitude,
                        default=configuration.LATITUDE,
                        help="The starting latitude")

    parser.add_argument("--longitude", action="store", type=argtypes.longitude,
                        default=configuration.LONGITUDE,
                        help="The starting longitude")

    parser.add_argument("--altitude", action="store", type=argtypes.altitude,
                        default=configuration.ALTITUDE,
                        help="The starting altitude")

    parser.add_argument("--airspeed", action="store", type=argtypes.airspeed,
                        default=configuration.AIRSPEED,
                        help="The starting airspeed")

    parser.add_argument("--heading", action="store", type=argtypes.heading,
                        default=configuration.HEADING,
                        help="The starting heading")

    parser.add_argument("--paused", action="store_true",
                        help="Start the simulator paused")

    return parser.parse_args()


def initialize_logger(output_file, debug):
    logger = logging.getLogger()

    logger_log_level = logging.INFO
    if debug:
        logger_log_level = logging.DEBUG

    logger.setLevel(logger_log_level)

    formater = logging.Formatter("%(asctime)s - %(module)s - "
                                 "%(levelname)s - %(message)s")

    if output_file:
        file_logging_handler = logging.FileHandler(output_file)
        file_logging_handler.setLevel(logger_log_level)
        file_logging_handler.setFormatter(formater)
        logger.addHandler(file_logging_handler)

    console_logging_handler = logging.StreamHandler()
    console_logging_handler.setLevel(logger_log_level)
    console_logging_handler.setFormatter(formater)
    logger.addHandler(console_logging_handler)

    return logger


def main():
    args = get_arguments()

    logger = initialize_logger(args.log, args.debug)

    logger.info("Starting the Huginn flight simulator")

    huginn_data_path = configuration.get_data_path()

    logger.debug("Selected trim mode is %s", args.trim)

    if args.paused:
        logger.info("The simulator will start paused")

    simulator_builder = SimulationBuilder(huginn_data_path)
    simulator_builder.trim_mode = TRIM_MODES[args.trim]
    simulator_builder.dt = args.dt

    simulator_builder.latitude = args.latitude
    simulator_builder.longitude = args.longitude
    simulator_builder.altitude = args.altitude
    simulator_builder.airspeed = args.airspeed
    simulator_builder.heading = args.heading
    simulator_builder.start_paused = args.paused

    logger.debug("Creating the simulator")
    simulator = simulator_builder.create_simulator()

    if not simulator:
        logger.error("Failed to create the simulator using the aircraft "
                     "model '%s'", args.aircraft)
        exit(1)

    initialize_controls_server(reactor, simulator.fdmexec, args.controls)
    initialize_simulator_data_server(reactor, simulator, args.fdm)

    initialize_websocket_server(
        reactor,
        simulator.fdm,
        configuration.WEBSOCKET_HOST,
        configuration.WEBSOCKET_PORT,
        configuration.WEBSOCKET_UPDATE_RATE
    )

    initialize_web_server(reactor, simulator, args.web)

    def run_simulator():
        result = simulator.run()

        if not result:
            logger.error("The simulator has failed to run")
            reactor.stop()

    fdm_updater = LoopingCall(run_simulator)
    fdm_updater.start(args.dt)

    logger.debug("starting the simulator server")
    reactor.run()
