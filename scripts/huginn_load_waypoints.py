#!/usr/bin/env python

from argparse import ArgumentParser

from huginn.configuration import WEB_SERVER_PORT
from huginn.clients import MapClient

def get_arguments():
    parser = ArgumentParser(description="Huginn flight simulator map control utility")
    
    parser.add_argument("--host", action="store", default="127.0.0.1", help="the simulator ip address")
    parser.add_argument("--port", action="store", default=WEB_SERVER_PORT, type=int, help="the simulator web server port")
    parser.add_argument("waypoint_file", action="store", help="the file containing the waypoints")

    return parser.parse_args()

def main():
    args = get_arguments()

    map_client = MapClient(args.host, args.port)

    result = map_client.load_from_csv(args.waypoint_file)

    if not result:
        print("Failed to load waypoints")

if __name__ == "__main__":
    main()