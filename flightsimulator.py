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
from flightsim.protocols import InterfaceInputProtocol, InterfaceOutputProtocol
from flightsim.rpc import FlightSimulatorRPC
from flightsim.web import Index, FDMData, Controls
from flightsim.configuration import InterfacesCatalog

DEFAULT_INTERFACES = {
    "rpc": {"host": "127.0.0.1", "port": 10500},
    "http": {"host": "127.0.0.1", "port": 8080}
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

def transmit_interface_data(protocol):
    protocol.transmit_interface_data()

def shutdown():
    reactor.callFromThread(reactor.stop)

def get_arguments(interface_catalog):
    parser = ArgumentParser(description="Flight Simulator")

    parser.add_argument("--properties", action="store_true", help="Print the property catalog")
    parser.add_argument("--rpc", action="store", default=interface_catalog.get_interface_port("rpc"), help="The XMLRPC port")
    parser.add_argument("--dt", action="store", default=0.0166, help="The simulation timestep")
    parser.add_argument("--http", action="store", default=interface_catalog.get_interface_port("http"), help="The web server port")
    parser.add_argument("--interface", action="append", help="The path to and interface file")

    return parser.parse_args()

def main():
    interface_catalog = init_interface_catalog(DEFAULT_INTERFACES)
    
    args = get_arguments(interface_catalog)

    dt = args.dt
    http_port = args.http

    fdmexec = FGFDMExec()

    package_filename = inspect.getfile(flightsim)
    package_path = path.dirname(package_filename)
    
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

    if args.properties:
        fdmexec.print_property_catalog()
        exit()

    rpc = FlightSimulatorRPC(fdmexec)

    rpc_port = args.rpc
    reactor.listenTCP(rpc_port, server.Site(rpc))

    index_page = Index(fdmexec)
    index_page.putChild("fdmdata", FDMData(fdmexec))
    index_page.putChild("controls", Controls(fdmexec))
    index_page.putChild("static", File(path.join(package_path, "static")))
    
    frontend = server.Site(index_page)
    reactor.listenTCP(http_port, frontend)

    for interface in args.interface:
        with open(interface) as f:
            interface_data = json.load(f)
            if interface_data.has_key("input"):
                properties = interface_data["input"]["properties"]
                input_port = interface_data["input"]["port"]
                if not interface_catalog.is_address_available("127.0.0.1", input_port):
                    print("Port %d is already in use" % input_port)
                    exit(-1)
                protocol = InterfaceInputProtocol(fdmexec, properties)
                reactor.listenUDP(input_port, protocol)
                interface_catalog.add("input:%s" % interface, "127.0.0.1", input_port)
            if interface_data.has_key("output"):
                data_rate = interface_data["output"]["dt"]
                properties = interface_data["output"]["properties"]
                output_address = interface_data["output"]["host"]
                output_port = interface_data["output"]["port"]
                if not interface_catalog.is_address_available(output_address, output_port):
                    print("Address %s:%d is already in use by another interface" % (output_address, output_port))
                    exit(-1)
                protocol = InterfaceOutputProtocol(fdmexec, output_address, output_port, properties)
                reactor.listenUDP(0, protocol)
                interface_catalog.add("output:%s" % interface, output_address, output_port)
                fdm_updater = task.LoopingCall(transmit_interface_data, protocol)
                fdm_updater.start(data_rate)

    fdm_updater = task.LoopingCall(update_fdm, fdmexec)
    fdm_updater.start(dt)

    signal.signal(signal.SIGTERM, shutdown)

    fdmexec.hold()

    reactor.run()
    
if __name__ == "__main__":
    main()
