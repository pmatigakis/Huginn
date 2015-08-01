#! python

import struct
from argparse import ArgumentParser

from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol

class FDMControlsProtocol(DatagramProtocol):
    def __init__(self, host, port, aileron, elevator, rudder, throttle):
        self.host = host
        self.port = port
        self.aileron = aileron
        self.elevator = elevator
        self.rudder = rudder
        self.throttle = throttle
    
    def startProtocol(self):
        controls_data = struct.pack("!ffff", self.elevator, self.aileron, self.rudder, self.throttle)
        self.transport.write(controls_data, (self.host, self.port))
        
        reactor.callFromThread(reactor.stop)

def get_arguments():
    parser = ArgumentParser(description="Flight simulator controls")
    
    parser.add_argument("host", help="the simulator ip address")
    parser.add_argument("port", type=int, help="the simulator port")
    
    parser.add_argument("aileron", type=float, help="aileron value")
    parser.add_argument("elevator", type=float, help="elevator value")
    parser.add_argument("rudder", type=float, help="rudder value")
    parser.add_argument("throttle", type=float, help="throttle value")
    
    return parser.parse_args()

def main():
    args = get_arguments()
    
    controls = FDMControlsProtocol(args.host,
                                   args.port,
                                   args.aileron,
                                   args.elevator,
                                   args.rudder,
                                   args.throttle)
    
    reactor.listenUDP(0, controls)
    reactor.run()

if __name__ == "__main__":
    main()