import csv
from argparse import ArgumentParser

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint

from huginn import configuration 
from huginn.protocols import TelemetryClientFactory
from huginn.validators import telemetry_endpoint

def get_arguments():
    parser = ArgumentParser(description="Huginn telemetry capturin utility")

    telemetry_port, telemetry_update_rate = telemetry_endpoint(configuration.TELEMETRY_ENDPOINT)

    parser.add_argument("--host", default="127.0.0.1", help="Huginn simulator address")
    parser.add_argument("--port", default=telemetry_port, help="Telemetry port")
    parser.add_argument("output", help="the output file")

    return parser.parse_args()

def main():
    args = get_arguments()

    with open(args.output, "w") as output_file:
        endpoint = TCP4ClientEndpoint(reactor, args.host, args.port)

        csv_writer = csv.writer(output_file, delimiter=",")

        factory = TelemetryClientFactory(csv_writer)

        endpoint.connect(factory)

        reactor.run()  # @UndefinedVariable

if __name__ == "__main__":
    main()