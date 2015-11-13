import logging
from argparse import ArgumentParser
import signal

from huginn import configuration
from huginn.fdm import create_fdmmodel
from huginn.simulator import Simulator
from huginn.validators import port_number, fdm_data_endpoint, telemetry_endpoint

def get_arguments():
    parser = ArgumentParser(description="Huginn flight simulator")

    parser.add_argument("--dt", action="store", type=float, default=configuration.DT, help="The simulation timestep")
    parser.add_argument("--telemetry", action="store", type=telemetry_endpoint, default=configuration.TELEMETRY_ENDPOINT, help="The telemetry endpoint")
    parser.add_argument("--http", action="store", type=port_number, default=configuration.WEB_SERVER_PORT, help="The web server port")
    parser.add_argument("--sensors", action="store", type=port_number, default=configuration.SENSORS_PORT, help="The sensors data port")
    parser.add_argument("--fdm", action="store", type=fdm_data_endpoint, default=configuration.FDM_ENDPOINT, help="The fdm data endpoint")
    parser.add_argument("--controls", action="store", type=port_number, default=configuration.CONTROLS_PORT, help="The controls port")
    parser.add_argument("--fdmmodel", action="store", default="jsbsim", help="The flight dynamics model to use")
    parser.add_argument("--aircraft", action="store", default="737", help="The aircraft model to use")
    parser.add_argument("--latitude", action="store", type=float, default=configuration.INITIAL_LATITUDE, help="The starting latitude")
    parser.add_argument("--longitude", action="store", type=float, default=configuration.INITIAL_LONGITUDE, help="The starting longitude")
    parser.add_argument("--altitude", action="store", type=float, default=configuration.INITIAL_ALTITUDE, help="The starting altitude")
    parser.add_argument("--airspeed", action="store", type=float, default=configuration.INITIAL_AIRSPEED, help="The starting airspeed")
    parser.add_argument("--heading", action="store", type=float, default=configuration.INITIAL_HEADING, help="The starting heading")

    return parser.parse_args()
    
def main():
    logging.basicConfig(format="%(asctime)s - %(module)s:%(levelname)s:%(message)s",
                        filename="huginn.log",
                        filemode="a",
                        level=logging.DEBUG)

    logging.info("Starting the Huginn flight simulator")

    args = get_arguments()

    fdm_model = create_fdmmodel(args.fdmmodel, args.aircraft, args.dt)

    if not fdm_model:
        logging.error("Failed to create flight model with name %s", args.fdmmodel)
        print("Failed to create flight model with name %s" % args.fdmmodel)
        exit(-1)

    initialization_result = fdm_model.load_initial_conditions(args.latitude,
                                                              args.longitude,
                                                              args.altitude,
                                                              args.airspeed,
                                                              args.heading)

    if not initialization_result:
        logging.error("Failed to create flight model with requested initial conditions")
        print("Failed to create flight model with requested initial conditions")
        exit(-1)

    trim_result = fdm_model.trim()
    
    if not trim_result:
        logging.error("Failed to trim the aircraft")
        print("Failed to trim the aircraft")
        exit(-1)

    simulator = Simulator(fdm_model)

    used_ports = set()

    fdm_host, fdm_port, fdm_dt = args.fdm 
    simulator.add_fdm_client(fdm_host, fdm_port, fdm_dt)
    used_ports.add(fdm_port)

    if args.sensors in used_ports:
        logging.error("Sensor port %d is already used", args.sensors)
        print("Sensor port %d is already used" % args.sensors)
        exit(-1)

    simulator.add_sensors_server(args.sensors)
    used_ports.add(args.sensors)

    if args.controls in used_ports:
        logging.error("Controls port %d is already used", args.controls)
        print("Controls port %d is already used" % args.controls)
        exit(-1)

    simulator.add_controls_server(args.controls)
    used_ports.add(args.controls)

    if args.http in used_ports:
        logging.error("Http port %d is already used", args.http)
        print("Http port %d is already used" % args.http)
        exit(-1)

    simulator.add_web_server(args.http)
    used_ports.add(args.http)

    telemetry_port, telemetry_update_rate = args.telemetry
    
    if telemetry_port in used_ports:
        logging.error("Telemetry port %d is already used", telemetry_port)
        print("Telemetry port %d is already used" % telemetry_port)
        exit(-1)

    simulator.add_telemetry_server(telemetry_port, telemetry_update_rate)

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
