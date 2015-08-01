#! python

from argparse import ArgumentParser
from os import path
import inspect
import signal
import json

from twisted.internet import reactor, task
from twisted.web import server
from twisted.web.static import File
from flightsimlib import FGFDMExec

import flightsim
from flightsim.protocols import FDMDataProtocol, ControlsProtocol
from flightsim.rpc import FlightSimulatorRPC
from flightsim.web import Index, FDMData, Controls
from flightsim.configuration import InterfacesCatalog

DEFAULT_INTERFACES = {
    "rpc": {"host": "127.0.0.1", "port": 10500},
    "http": {"host": "127.0.0.1", "port": 8080},
    "fdm": {"host": "127.0.0.1", "port": 10300},
    "controls": {"host": "127.0.0.1", "port": 10301}
}

def init_interface_catalog(default_interfaces):
    interface_catalog = InterfacesCatalog()
    
    for interface in default_interfaces:
        address = default_interfaces[interface]["host"]
        port = default_interfaces[interface]["port"]
        
        interface_catalog.add(interface, address, port)
        
    return interface_catalog

def update_fdm(fdmexec):
    fdmexec.run()

def shutdown():
    reactor.callFromThread(reactor.stop)

def get_arguments(interface_catalog):
    parser = ArgumentParser(description="Flight Simulator")

    parser.add_argument("--properties", action="store_true", help="Print the property catalog")
    parser.add_argument("--rpc", action="store", default=interface_catalog.get_interface_port("rpc"), help="The XMLRPC port")
    parser.add_argument("--dt", action="store", default=0.0166, help="The simulation timestep")
    parser.add_argument("--http", action="store", default=interface_catalog.get_interface_port("http"), help="The web server port")
    parser.add_argument("--fdm", action="store", default=interface_catalog.get_interface_port("fdm"), help="The fdm data port")
    parser.add_argument("--controls", action="store", default=interface_catalog.get_interface_port("controls"), help="The controls port")

    return parser.parse_args()

def init_fdm(dt, package_path):
    fdmexec = FGFDMExec()
    
    fdmexec.set_root_dir(package_path + "/data/")
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
        print("Failed to run initial condition")
        exit(-1)

    running = fdmexec.run()
    while running and fdmexec.get_sim_time() < 0.1:
        fdmexec.process_message()
        fdmexec.check_incremental_hold()

        running = fdmexec.run()
        
    result = fdmexec.trim()    
    if not result:
        print("Failed to trim the aircraft")
        exit(-1)
        
    return fdmexec

def init_rpc_server(args, fdmexec):
    rpc = FlightSimulatorRPC(fdmexec)

    rpc_port = args.rpc
    reactor.listenTCP(rpc_port, server.Site(rpc))

def init_web_server(args, fdmexec, package_path):
    index_page = Index(fdmexec)
    index_page.putChild("fdmdata", FDMData(fdmexec))
    index_page.putChild("controls", Controls(fdmexec))
    index_page.putChild("static", File(path.join(package_path, "static")))
    
    http_port = args.http
    frontend = server.Site(index_page)
    reactor.listenTCP(http_port, frontend)

def init_fdm_server(args, fdmexec):
    fdm_protocol = FDMDataProtocol(fdmexec)
    fdm_port = args.fdm
    reactor.listenUDP(fdm_port, fdm_protocol)

    controls_protocol = ControlsProtocol(fdmexec) 
    controls_port = args.controls
    reactor.listenUDP(controls_port, controls_protocol)

def main():
    interface_catalog = init_interface_catalog(DEFAULT_INTERFACES)
    
    args = get_arguments(interface_catalog)

    package_filename = inspect.getfile(flightsim)
    package_path = path.dirname(package_filename)

    dt = args.dt

    fdmexec = init_fdm(dt, package_path)

    if args.properties:
        fdmexec.print_property_catalog()
        exit()

    init_rpc_server(args, fdmexec)
    
    init_web_server(args, fdmexec, package_path)

    init_fdm_server(args, fdmexec)

    fdm_updater = task.LoopingCall(update_fdm, fdmexec)
    fdm_updater.start(dt)

    signal.signal(signal.SIGTERM, shutdown)

    fdmexec.hold()

    reactor.run()
    
if __name__ == "__main__":
    main()
