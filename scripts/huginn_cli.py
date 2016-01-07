#!/usr/bin/env python

from argparse import ArgumentParser

from huginn.commands import DataCommand, ControlCommand, LoadWaypointsCommand,\
                            TelemetryCommand
from huginn import configuration

def main():
    parser = ArgumentParser(description="Huginn flight simulator command line tool")

    parser.add_argument("--host", action="store", default="127.0.0.1", help="the simulator ip address")
    parser.add_argument("--web_port", action="store", default=configuration.WEB_SERVER_PORT, type=int, help="the flight dynamics model http port")

    subparsers = parser.add_subparsers()

    data_command = DataCommand()
    data_command.register_command(subparsers)

    control_command = ControlCommand()
    control_command.register_command(subparsers)

    load_waypoints_command = LoadWaypointsCommand()
    load_waypoints_command.register_command(subparsers)

    telemetry_command = TelemetryCommand()
    telemetry_command.register_command(subparsers)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()