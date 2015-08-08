import struct

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

fdm_data_properties = ["accelerations/a-pilot-x-ft_sec2",
                       "accelerations/a-pilot-y-ft_sec2",
                       "accelerations/a-pilot-z-ft_sec2",
                       "velocities/p-rad_sec",
                       "velocities/q-rad_sec",
                       "velocities/r-rad_sec",
                       "atmosphere/P-psf",
                       "aero/qbar-psf",
                       "atmosphere/T-R",
                       "position/lat-gc-deg",
                       "position/long-gc-deg",
                       "position/h-sl-ft",
                       "velocities/vtrue-kts",
                       "attitude/heading-true-rad"]

fdm_control_properties = [
    "fcs/elevator-cmd-norm",
    "fcs/aileron-cmd-norm",
    "fcs/rudder-cmd-norm",
    "fcs/throttle-cmd-norm"
]

class FDMDataProtocol(DatagramProtocol):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
        
    def datagramReceived(self, datagram, (host, port)):
        fdm_data = [self.fdmexec.get_property_value(fdm_property)
                    for fdm_property in fdm_data_properties]
        
        fdm_data_string = struct.pack("!" + "f" * len(fdm_data_properties), *fdm_data)
        
        self.transport.write(fdm_data_string, (host, port))
    
class ControlsProtocol(DatagramProtocol):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
    
    def datagramReceived(self, datagram, addr):
        try:
            controls_data = struct.unpack("!ffff", datagram)
        
            for index, control_property in enumerate(fdm_control_properties):
                self.fdmexec.set_property_value(control_property, controls_data[index])
        except struct.error:
            print("Failed to parse control data")

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