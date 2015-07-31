#! python

import struct
from argparse import ArgumentParser

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

from flightsim.protocols import fdm_data_properties

class FDMDataClientProtocol(DatagramProtocol):
    def __init__(self, host, port):
        self.host = host
        self.port = port
    
    def startProtocol(self):
        self.transport.write("\n", (self.host, self.port))
    
    def datagramReceived(self, datagram, addr):
        try:
            fdm_data = struct.unpack("!" + "f" * len(fdm_data_properties), datagram)
            for index, fdm_property in enumerate(fdm_data_properties):
                print("%s\t%f" % (fdm_property, fdm_data[index]))
        except struct.error:
            print("Failed to parse received data")
        finally:
            reactor.callFromThread(reactor.stop)

def get_arguments():
    parser = ArgumentParser(description="Flight simulator data reader")
    
    parser.add_argument("host", help="the simulator ip address")
    parser.add_argument("port", type=int, help="the simulator port")
    
    return parser.parse_args()

def main():
    args = get_arguments()
    
    protocol = FDMDataClientProtocol(args.host, args.port)
    reactor.listenUDP(0, protocol)
    reactor.run()
    
if __name__ == "__main__":
    main()