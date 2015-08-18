from argparse import ArgumentParser

from twisted.internet import reactor

from huginn.configuration import HUGINN_HOST, FDM_PORT
from huginn.protocols import FDMDataClientProtocol

def get_arguments():
    parser = ArgumentParser(description="Huginn flight simulator data viewer")
    
    parser.add_argument("--host", action="store", default=HUGINN_HOST, help="the simulator ip address")
    parser.add_argument("--port", action="store", default=FDM_PORT, type=int, help="the flight dynamics model data port")

    return parser.parse_args()

def main():
    args = get_arguments()

    protocol = FDMDataClientProtocol(args.host, args.port)
    reactor.listenUDP(0, protocol)
    reactor.run()

if __name__ == "__main__":
    main()