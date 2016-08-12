from argparse import ArgumentParser

from huginn.cli import argtypes
from huginn.clients import MapClient
from huginn import configuration


def execute_add_waypoint(args):
    client = MapClient(args.host, args.port)

    result = client.add_waypoint(args.name, args.latitude, args.longitude,
                                 args.altitude)

    if result is None:
        print("Failed to add waypoint")
        exit(1)


def execute_delete_waypoint(args):
    client = MapClient(args.host, args.port)

    result = client.delete_waypoint(args.name)

    if result is None:
        print("Failed to delete waypoint")
        exit(1)


def execute_load_waypoints(args):
    client = MapClient(args.host, args.port)

    result = client.load(args.filename)

    if result is None:
        print("Failed to load waypoints from file")
        exit(1)


def get_arguments():
    parser = ArgumentParser(description="Waypoint management tool")

    parser.add_argument("--host", default="localhost",
                        help="the huginn host")
    parser.add_argument("--port", type=argtypes.port_number,
                        default=configuration.WEB_SERVER_PORT)

    subparsers = parser.add_subparsers(help="Sub-command help")

    add_parser = subparsers.add_parser("add", help="Add a waypoint")
    add_parser.add_argument("name", help="the waypoint name")
    add_parser.add_argument("latitude", type=argtypes.latitude,
                            help="the waypoint latitude")
    add_parser.add_argument("longitude", type=argtypes.longitude,
                            help="the waypoint longitude")
    add_parser.add_argument("altitude", type=argtypes.altitude,
                            help="the waypoint altitude")
    add_parser.set_defaults(func=execute_add_waypoint)

    delete_parser = subparsers.add_parser("delete", help="delete a waypoint")
    delete_parser.add_argument("name", help="the waypoint name")
    delete_parser.set_defaults(func=execute_delete_waypoint)

    load_parser = subparsers.add_parser(
        "load", help="Load a list of waypoints from a file")
    load_parser.add_argument("filename", help="the waypoint file")
    load_parser.set_defaults(func=execute_load_waypoints)

    return parser.parse_args()


def main():
    args = get_arguments()

    args.func(args)
