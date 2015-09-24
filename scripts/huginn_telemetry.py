from argparse import ArgumentParser

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint

from huginn import configuration 
from huginn.protocols import TelemetryClientFactory

def get_arguments():
    parser = ArgumentParser(description="Huginn telemetry capturin utility")

    parser.add_argument("--host", default=configuration.HUGINN_HOST, help="Huginn simulator address")
    parser.add_argument("--port", default=configuration.TELEMETRY_PORT, help="Telemetry port")
    parser.add_argument("output", help="the output file")

    return parser.parse_args()

def main():
    args = get_arguments()

    output_file = open(args.output, "w")

    endpoint = TCP4ClientEndpoint(reactor, args.host, args.port)

    factory = TelemetryClientFactory(output_file)

    endpoint.connect(factory)

    reactor.run()

    output_file.close()

if __name__ == "__main__":
    main()