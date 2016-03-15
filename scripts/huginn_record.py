#!/usr/bin/env python

from argparse import ArgumentParser

import json
from twisted.internet import reactor
from twisted.web.client import Agent, readBody
from twisted.web.http_headers import Headers
from twisted.internet.task import LoopingCall

from huginn import configuration
from huginn.io import CSVFDMDataWriter, FDMDataPrinter

def get_arguments():
    parser = ArgumentParser(description="Record the fdm data")

    parser.add_argument("--host", action="store", default="127.0.0.1", help="the simulator ip address")
    parser.add_argument("--port", action="store", default=configuration.WEB_SERVER_PORT, type=int, help="the simulator http port")

    parser.add_argument("--dt", default=1.0, help="How often to request data from the simulator")
    parser.add_argument("output", help="the output file")

    return parser.parse_args()

def request_fdm_data(args, csv_telemetry_writer):
    agent = Agent(reactor)

    url = "http://%s:%d/fdm" % (args.host, args.port)

    d = agent.request("GET",
                      url,
                      Headers({}),
                      None)

    d.addCallback(process_fdm_data_response, csv_telemetry_writer)

    return d

def process_fdm_data_response(response, csv_telemetry_writer):
        d = readBody(response)
        d.addCallback(save_fdm_data, csv_telemetry_writer)
        return d

def save_fdm_data(body, csv_telemetry_writer):
    fdm_data = json.loads(body)

    csv_telemetry_writer.write_fdm_data(fdm_data)

    for variable in ["time", "altitude", "airspeed", "heading"]:
        print("%s\t%f" % (variable, fdm_data[variable]))
    print ("")

def main():
    args = get_arguments()

    #fdm_data_printer = FDMDataPrinter(["time", "altitude", "airspeed", "heading"])

    output_file = open(args.output, "w")

    variables = ["time", "dt", "latitude", "longitude", "altitude",
                 "airspeed", "heading", "x_acceleration", "y_acceleration",
                 "z_acceleration", "roll_rate", "pitch_rate", "yaw_rate",
                 "temperature", "static_pressure", "total_pressure",
                 "roll", "pitch", "thrust", "aileron", "elevator","rudder",
                 "throttle"]

    csv_telemetry_writer = CSVFDMDataWriter(variables, output_file)
    csv_telemetry_writer.write_header()

    task = LoopingCall(request_fdm_data, args, csv_telemetry_writer)
    task.start(args.dt)

    reactor.run()  # @UndefinedVariable

    output_file.close()

if __name__ == "__main__":
    main()