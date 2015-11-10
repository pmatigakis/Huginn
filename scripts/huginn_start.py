import os
import logging
from argparse import ArgumentParser
import signal

from huginn import configuration
from huginn.fdm import JSBSimFDMModelCreator
from huginn.simulator import Simulator

def get_arguments():
    parser = ArgumentParser(description="Huginn flight simulator")

    parser.add_argument("--dt", action="store", default=configuration.DT, help="The simulation timestep")
    parser.add_argument("--telemetry", action="store", default=configuration.TELEMETRY_PORT, help="The telemetry port")
    parser.add_argument("--telemetry_dt", action="store", default=configuration.TELEMETRY_UPDATE_RATE, help="The telemetry update rate")
    parser.add_argument("--http", action="store", default=configuration.WEB_SERVER_PORT, help="The web server port")
    parser.add_argument("--sensors", action="store", default=configuration.SENSORS_PORT, help="The sensors data port")
    parser.add_argument("--fdm_host", action="store", default=configuration.FDM_HOST, help="The fdm data host")
    parser.add_argument("--fdm_port", action="store", default=configuration.FDM_PORT, help="The fdm data port")
    parser.add_argument("--fdm_dt", action="store", default=configuration.FDM_DT, help="The fdm data dt")
    parser.add_argument("--controls", action="store", default=configuration.CONTROLS_PORT, help="The controls port")
    parser.add_argument("--fdmmodel", action="store", default="jsbsim", help="The flight dynamics model to use")

    return parser.parse_args()

def get_fdm_creator(args):
    fdm_name = args.fdmmodel
    
    if fdm_name == "jsbsim":
        dt = args.dt

        jsbsim_path = os.environ.get("JSBSIM_HOME", None)

        if not jsbsim_path:
            logging.error("The JSBSIM_HOME environment variable is not set")
            print("The JSBSIM_HOME environment variable is not set")
            return None

        return JSBSimFDMModelCreator(jsbsim_path, dt)
    else:
        return None
    
def main():
    logging.basicConfig(format="%(asctime)s - %(module)s:%(levelname)s:%(message)s",
                        filename="huginn.log",
                        filemode="a",
                        level=logging.DEBUG)

    logging.info("Starting the Huginn flight simulator")

    args = get_arguments()

    fdm_model_creator = get_fdm_creator(args)

    if not fdm_model_creator:
        logging.error("Failed to create flight model with name %s", args.fdmmodel)
        print("Failed to create flight model with name %s" % args.fdmmodel)
        exit(-1)

    fdm_model = fdm_model_creator.create_fdm_model()

    initialization_result = fdm_model.load_initial_conditions(configuration.INITIAL_LATITUDE,
                                                              configuration.INITIAL_LONGITUDE,
                                                              configuration.INITIAL_ALTITUDE,
                                                              configuration.INITIAL_AIRSPEED,
                                                              configuration.INITIAL_HEADING)

    if not initialization_result:
        logging.error("Failed to create flight model with requested initial conditions")
        print("Failed to create flight model with requested initial conditions")
        exit(-1)

    simulator = Simulator(fdm_model)

    simulator.add_fdm_client(args.fdm_host, args.fdm_port, args.fdm_dt)
    simulator.add_sensors_server(args.sensors)
    simulator.add_controls_server(args.controls)
    simulator.add_web_server(args.http)
    simulator.add_telemetry_server(args.telemetry, args.telemetry_dt)

    signal.signal(signal.SIGTERM, simulator.shutdown)

    logging.debug("Starting the simulator")

    result = simulator.run()

    if result:
        logging.info("The simulator has shut down")
    else:
        logging.info("The simulator has encountered an error and stopped")
        print("The simulator has encountered an error and stopped")
        exit(-1)

if __name__ == "__main__":
    main()
