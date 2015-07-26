from twisted.internet.protocol import DatagramProtocol

class InterfaceOutputProtocol(DatagramProtocol):
    def __init__(self, fdmexec, address, port, output_properties):
        self.fdmexec = fdmexec
        self.address = address
        self.port = port
        self.output_properties = output_properties

    def transmit_interface_data(self):
        output_data = [self.fdmexec.get_property_value(str(property_name))
                       for property_name in self.output_properties]

        output_data = map(str, output_data)
                    
        packet = ",".join(output_data) + "\r\n"

        self.transport.write(packet, (self.address, self.port))

class InterfaceInputProtocol(DatagramProtocol):
    def __init__(self, fdmexec, input_properties):
        self.fdmexec = fdmexec
        self.input_properties = input_properties
        
    def datagramReceived(self, data, (host, port)):
        input_data = data.strip().split(",")
        input_data = map(float, input_data)

        for i, property_name in enumerate(self.input_properties):
            self.fdmexec.set_property_value(property_name, input_data[i])