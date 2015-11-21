import logging
from argparse import ArgumentParser
import signal
import os

from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from huginn import configuration
from huginn.simulator import Simulator
from huginn.validators import port_number, fdm_data_endpoint, telemetry_endpoint
from huginn.fdm import create_aircraft_model
from huginn.network import WebServer, TelemetryServer, SensorsServer, ControlsServer, FDMDataServer

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
    parser.add_argument("--sensors", action="store", type=port_number, default=configuration.SENSORS_PORT, help="The sensors data port")
    
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

    aircraft = create_aircraft_model(jsbsim_path, args.aircraft, args.dt)

    if not aircraft:
        logging.error("Failed to create flight model with name %s using the aircraft %s", args.fdmmodel, args.aircraft)
        print("Failed to create flight model with name %s using the aircraft %s" % args.fdmmodel, args.aircraft)
        exit(-1)

    aircraft.set_initial_conditions(args.latitude,
                                    args.longitude,
                                    args.altitude,
                                    args.airspeed,
                                    args.heading)

    simulator = Simulator(aircraft)

    reset_result = simulator.reset()
    
    if not reset_result:
        logging.error("Failed to reset the simulation")
        print("Failed to reset the simulation")
        exit(-1)

    fdm_client_address, fdm_client_port, fdm_client_update_rate = args.fdm 

    fdm_data_server = FDMDataServer(aircraft, fdm_client_address, fdm_client_port, fdm_client_update_rate)
    fdm_data_server.start()

    used_ports = set()
    
    sensors_server = SensorsServer(aircraft, args.sensors)
    sensors_server.start()
    used_ports.add(args.sensors)

    if args.controls in used_ports:
        logging.error("Controls port %d is already used", args.controls)
        print("Controls port %d is already used" % args.controls)
        exit(-1)

    controls_server = ControlsServer(aircraft, args.controls)
    controls_server.start()
    used_ports.add(args.controls)

    if args.http in used_ports:
        logging.error("Http port %d is already used", args.http)
        print("Http port %d is already used" % args.http)
        exit(-1)

    web_server = WebServer(simulator, aircraft, args.http) 
    web_server.start()
    used_ports.add(args.http)

    telemetry_port, telemetry_update_rate = args.telemetry
    
    if telemetry_port in used_ports:
        logging.error("Telemetry port %d is already used", telemetry_port)
        print("Telemetry port %d is already used" % telemetry_port)
        exit(-1)

    telemetry_server = TelemetryServer(aircraft, telemetry_port, telemetry_update_rate)
    telemetry_server.start()

    signal.signal(signal.SIGTERM, shutdown)

    fdm_updater = LoopingCall(simulator.run)
    fdm_updater.start(simulator.dt)

    logging.debug("Starting the event loop")
    reactor.run() # @UndefinedVariable
    logging.info("The simulator has shut down")

if __name__ == "__main__":
    main()
