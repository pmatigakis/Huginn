#! python

from argparse import ArgumentParser
from os import path
import inspect
import signal

from twisted.internet import reactor, task
from twisted.web import server
from flightsimlib import FGFDMExec

import flightsim
from flightsim.protocols import FlightSimulatorProtocol
from flightsim.rpc import FlightSimulatorRPC
        
def update_fdm(protocol):
    protocol.update_fdm()

def transmit_fdm_data(protocol):
    protocol.transmit_fdm_data()

def shutdown():
    reactor.callFromThread(reactor.stop)

def get_arguments():
    parser = ArgumentParser(description="Flight Simulator")

    parser.add_argument("--properties", action="store_true", help="Print the property catalog")
    #parser.add_argument("simulation_file", help="Simulation definition file")
    parser.add_argument("--rpc", action="store", default=10500, help="The XMLRPC port")
    parser.add_argument("--controls", action="store", default=10501, help="The controls port")
    parser.add_argument("--fdm_address", action="store", default="127.0.0.1", help="The FDM data remote address")
    parser.add_argument("--fdm_port", action="store", default=10502, help="The FDM data port")
    parser.add_argument("--dt", action="store", default=0.0166, help="The simulation timestep")
    parser.add_argument("--fdm_data_rate", action="store", default=0.1, help="The fdm data transmit rate")

    return parser.parse_args()

def main():
    args = get_arguments()

    dt = args.dt
    fdm_data_rate = args.fdm_data_rate

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

    protocol = FlightSimulatorProtocol(fdmexec, args)

    rpc = FlightSimulatorRPC(fdmexec)

    rpc_port = args.rpc
    reactor.listenTCP(rpc_port, server.Site(rpc))

    input_port = args.controls

    reactor.listenUDP(input_port, protocol)

    fdm_updater = task.LoopingCall(update_fdm, protocol)
    fdm_updater.start(dt)

    fdm_updater = task.LoopingCall(transmit_fdm_data, protocol)
    fdm_updater.start(fdm_data_rate)

    signal.signal(signal.SIGTERM, shutdown)

    fdmexec.hold()

    reactor.run()
    
if __name__ == "__main__":
    main()
