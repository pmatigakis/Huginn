from argparse import ArgumentParser

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint

from huginn import configuration 
from huginn.protocols import TelemetryClientFactory
from huginn.io import CSVTelemetryWriter, TelemetryPrinter

def get_arguments():
    parser = ArgumentParser(description="Huginn telemetry capturin utility")

    parser.add_argument("--host", default="127.0.0.1", help="Huginn simulator address")
    parser.add_argument("--port", default=configuration.TELEMETRY_PORT, help="Telemetry port")
    parser.add_argument("output", help="the output file")

    return parser.parse_args()

def main():
    args = get_arguments()

    endpoint = TCP4ClientEndpoint(reactor, args.host, args.port)

    factory = TelemetryClientFactory()

    endpoint.connect(factory)

    with open(args.output, "w") as output_file:    
        csv_telemetry_writer = CSVTelemetryWriter(output_file)
        factory.add_telemetry_listener(csv_telemetry_writer)

        telemetry_printer = TelemetryPrinter(
            variables=["time", "latitude", "longitude", "altitude", "airspeed",
                       "heading"]
        )

        factory.add_telemetry_listener(telemetry_printer)

        reactor.run()  # @UndefinedVariable

if __name__ == "__main__":
    main()