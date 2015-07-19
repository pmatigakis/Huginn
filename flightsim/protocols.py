from twisted.internet.protocol import DatagramProtocol
#from twisted.internet import reactor

from flightsim.fdm import controls_properties, fdm_properties

class FlightSimulatorProtocol(DatagramProtocol):
    def __init__(self, fdmexec, args):
        self.fdmexec = fdmexec
        self.args = args
        self.running = False
        
    def datagramReceived(self, data, (host, port)):
        controls_data = data.strip().split(",")
        controls_data = map(float, controls_data)

        for i, property_name in enumerate(controls_properties):
            self.fdmexec.set_property_value(property_name, controls_data[i])

    def update_fdm(self):
        self.running = self.fdmexec.run()

    def transmit_fdm_data(self):
        if self.running:
            output_data = [self.fdmexec.get_property_value(str(property_name))
                           for property_name in fdm_properties]

            output_data = map(str, output_data)
                    
            packet = ",".join(output_data) + "\r\n"

            self.transport.write(packet, (self.args.fdm_address, self.args.fdm_port))
#        else:
#            reactor.callFromThread(reactor.stop)