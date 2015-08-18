from os import path
import logging
from argparse import ArgumentParser
import inspect
import signal

from twisted.internet import reactor, task
from twisted.web import server
from flightsimlib import FGFDMExec

import huginn
from huginn.protocols import FDMDataProtocol, ControlsProtocol
from huginn.http import Index, FDMData, Controls
from huginn.rpc import FlightSimulatorRPC
from huginn.configuration import CONTROLS_PORT, FDM_PORT, RPC_PORT, WEB_SERVER_PORT, DT

def get_arguments():
    parser = ArgumentParser(description="Huginn flight simulator")
    
    parser.add_argument("--properties", action="store_true", help="Print the property catalog")
    parser.add_argument("--rpc", action="store", default=RPC_PORT, help="The XMLRPC port")
    parser.add_argument("--dt", action="store", default=DT, help="The simulation timestep")
    parser.add_argument("--http", action="store", default=WEB_SERVER_PORT, help="The web server port")
    parser.add_argument("--fdm", action="store", default=FDM_PORT, help="The fdm data port")
    parser.add_argument("--controls", action="store", default=CONTROLS_PORT, help="The controls port")
    
    return parser.parse_args()

def create_fdm(dt, package_path):
    logging.debug("Initializing the flight dynamics model")
    
    fdmexec = FGFDMExec()
    
    jsbsim_data_path = path.join(package_path, "data/")
    
    logging.debug("Using jsbsim data at %s", jsbsim_data_path)
    
    fdmexec.set_root_dir(jsbsim_data_path)
    fdmexec.set_aircraft_path("aircraft")
    fdmexec.set_engine_path("engine")
    fdmexec.set_systems_path("systems")

    fdmexec.set_dt(dt)

    fdmexec.load_model("c172p")

    fdmexec.load_ic("reset01")

    fdmexec.set_property_value("fcs/throttle-cmd-norm", 0.65)
    fdmexec.set_property_value("fcs/mixture-cmd-norm", 0.87)
    fdmexec.set_property_value("propulsion/magneto_cmd", 3.0)
    fdmexec.set_property_value("propulsion/starter_cmd", 1.0)

    initial_condition_result = fdmexec.run_ic()

    if not initial_condition_result:
        logging.error("Failed to set the flight dynamics model's initial condition")
        print("Failed to set the flight dynamics model's initial condition")
        exit(-1)

    running = fdmexec.run()
    
    if not running:
        logging.error("Failed to make initial flight dynamics model run")
        print("Failed to make initial flight dynamics model run")
        exit(-1)
    
    while running and fdmexec.get_sim_time() < 0.1:
        fdmexec.process_message()
        fdmexec.check_incremental_hold()

        running = fdmexec.run()
        
    result = fdmexec.trim()    
    if not result:
        logging.error("Failed to trim the aircraft")
        print("Failed to trim the aircraft")
        exit(-1)
        
    return fdmexec

def init_rpc_server(args, fdmexec):        
    rpc = FlightSimulatorRPC(fdmexec)

    rpc_port = args.rpc
    
    logging.debug("Starting the RPC server at port %d", rpc_port)
    
    reactor.listenTCP(rpc_port, server.Site(rpc))

def init_web_server(args, fdmexec, package_path):
    index_page = Index(fdmexec)
    index_page.putChild("fdmdata", FDMData(fdmexec))
    index_page.putChild("controls", Controls(fdmexec))
    
    http_port = args.http
    
    logging.debug("Starting the web server at port %d", http_port)
    
    frontend = server.Site(index_page)
    reactor.listenTCP(http_port, frontend)

def init_fdm_server(args, fdmexec):
    fdm_protocol = FDMDataProtocol(fdmexec)
    fdm_port = args.fdm
    
    logging.debug("Starting the flight dynamics model server at port %d", fdm_port)
    
    reactor.listenUDP(fdm_port, fdm_protocol)

    controls_protocol = ControlsProtocol(fdmexec) 
    controls_port = args.controls
    
    logging.debug("Starting the aircraft controls server at port %d", controls_port)
    
    reactor.listenUDP(controls_port, controls_protocol)

def update_fdm(fdmexec):
    fdmexec.process_message()
    fdmexec.check_incremental_hold()
    running = fdmexec.run()
    
    if not running:
        logging.error("Failed to update the flight dynamics model")
        print("Failed to update the flight dynamics model")
        shutdown()
        
def shutdown():
    logging.debug("Shutting down Huginn")
    
    reactor.callFromThread(reactor.stop)

def main():
    logging.basicConfig(format="%(asctime)s - %(module)s:%(levelname)s:%(message)s",
                        filename="huginn.log", 
                        filemode="a", 
                        level=logging.DEBUG)

    logging.info("Starting the Huginn flight simulator")
    
    args = get_arguments()
        
    dt = args.dt

    package_filename = inspect.getfile(huginn)
    package_path = path.dirname(package_filename)

    fdmexec = create_fdm(dt, package_path)

    init_rpc_server(args, fdmexec)
    init_fdm_server(args, fdmexec)
    init_web_server(args, fdmexec, package_path)
    
    fdm_updater = task.LoopingCall(update_fdm, fdmexec)
    fdm_updater.start(dt)

    signal.signal(signal.SIGTERM, shutdown)

    fdmexec.hold()

    logging.debug("Starting the event loop")
    reactor.run()
    logging.info("The simulator has shut down")

if __name__ == "__main__":
    main()