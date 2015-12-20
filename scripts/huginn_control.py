#!/usr/bin/env python

from argparse import ArgumentParser

from huginn.configuration import WEB_SERVER_PORT
from huginn.control import SimulatorControlClient

def get_arguments():
    parser = ArgumentParser(description="Huginn flight simulator control")
    
    parser.add_argument("--host", action="store", default="127.0.0.1", help="the simulator ip address")
    parser.add_argument("--port", action="store", default=WEB_SERVER_PORT, type=int, help="the flight dynamics RPC port")
    parser.add_argument("command", action="store",
                        choices=["pause", "resume", "reset"], 
                        help="the simulator control command")

    return parser.parse_args()

def main():
    args = get_arguments()

    simulator_control_client = SimulatorControlClient(args.host, args.port)

    if args.command == "reset":
        result = simulator_control_client.reset()
    elif args.command == "pause":
        result = simulator_control_client.pause()
    elif args.command == "resume":
        result = simulator_control_client.resume()
    else:
        print("Invalid command %s" % args.command)
        exit(-1)

    if not result:
        print("Failed to execute command %s" % args.command)
        exit(-1)

if __name__ == "__main__":
    main()
