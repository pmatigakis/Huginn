import struct

from twisted.internet.protocol import DatagramProtocol

fdm_data_properties = ["accelerations/a-pilot-x-ft_sec2",
                       "accelerations/a-pilot-y-ft_sec2",
                       "accelerations/a-pilot-z-ft_sec2",
                       "accelerations/pdot-rad_sec2",
                       "accelerations/qdot-rad_sec2",
                       "accelerations/rdot-rad_sec2",
                       "atmosphere/P-psf",
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