import struct
from argparse import ArgumentParser

from twisted.internet import reactor

from huginn.configuration import HUGINN_HOST, SIMULATOR_CONTROL_PORT
from huginn.protocols import (SIMULATION_PAUSE, SIMULATION_RESET,
                              SIMULATION_RESUME, SimulatorControlClient)

def get_arguments():
    parser = ArgumentParser(description="Huginn flight simulator control")
    
    parser.add_argument("--host", action="store", default=HUGINN_HOST, help="the simulator ip address")
    parser.add_argument("--port", action="store", default=SIMULATOR_CONTROL_PORT, type=int, help="the flight dynamics RPC port")
    parser.add_argument("command", action="store", help="the simulator control command")

    return parser.parse_args()

def main():
    args = get_arguments()
    
    if args.command == "resume":
        request_code = SIMULATION_RESUME
    elif args.command == "pause":
        request_code = SIMULATION_PAUSE
    elif args.command == "reset":
        request_code = SIMULATION_RESET
    else:
        print("Invalid command %s" % args.command)
        exit()

    protocol = SimulatorControlClient(args.host, args.port, request_code)

    reactor.listenUDP(0, protocol)
    
    reactor.run()

if __name__ == "__main__":
    main()