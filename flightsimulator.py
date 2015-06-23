#! python

from os import path
import inspect
from argparse import ArgumentParser
from datetime import datetime, timedelta
from Queue  import Queue
import time
import json
import signal

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor, task
from twisted.web import server
from twisted.web.xmlrpc import XMLRPC

from flightsimlib import FGFDMExec
import flightsim
from flightsim.fdm import controls_properties, fdm_properties

class FlightSimulatorRPC(XMLRPC):
    def __init__(self, fdmexec):
        XMLRPC.__init__(self)

        self.fdmexec = fdmexec
        
    def xmlrpc_pause(self):
        self.fdmexec.hold()

        return True

    def xmlrpc_unpause(self):
        self.fdmexec.resume()

        return True

    def xmlrpc_reset(self):
        return self.fdmexec.run_ic()

class FlightSimulatorProtocol(DatagramProtocol):
    def __init__(self, fdmexec, simulation_settings):
        self.fdmexec = fdmexec
        self.simulation_settings = simulation_settings
        
    def datagramReceived(self, data, (host, port)):
        controls_data = data.strip().split(",")
        controls_data = map(float, controls_data)

        for i, property_name in enumerate(controls_properties):
            self.fdmexec.set_property_value(property_name, controls_data[i])

    def update_fdm(self):
        running = self.fdmexec.run()

        if running:
            output_data = [self.fdmexec.get_property_value(str(property_name))
                           for property_name in fdm_properties]

            output_data = map(str, output_data)
                    
            packet = ",".join(output_data) + "\r\n"

            for host, port in self.simulation_settings["output"]["addresses"]:
                self.transport.write(packet, (host, port))
        else:
            reactor.callFromThread(reactor.stop)
        
def update_fdm(protocol):
    protocol.update_fdm()
    
def shutdown():
    reactor.callFromThread(reactor.stop)

def get_arguments():
    parser = ArgumentParser(description="Flight Simulator")

    parser.add_argument("--properties", action="store_true", help="Print the property catalog")
    parser.add_argument("simulation_file", help="Simulation definition file")

    return parser.parse_args()

def main():
    args = get_arguments()

    simulation_file = args.simulation_file

    with open(simulation_file) as f:
        simulation_settings = json.load(f)

    dt = simulation_settings["dt"]

    print("Using dt: %f" % dt)

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

    protocol = FlightSimulatorProtocol(fdmexec, simulation_settings)

    rpc = FlightSimulatorRPC(fdmexec)

    rpc_port = simulation_settings["rpc"]["port"]
    reactor.listenTCP(rpc_port, server.Site(rpc))

    input_port = simulation_settings["input"]["port"]

    reactor.listenUDP(input_port, protocol)

    fdm_updater = task.LoopingCall(update_fdm, protocol)
    fdm_updater.start(dt)

    signal.signal(signal.SIGTERM, shutdown)

    reactor.run()
    
if __name__ == "__main__":
    main()
