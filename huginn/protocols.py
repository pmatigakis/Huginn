import struct
import logging

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

from huginn.fdm import fdm_data_properties, controls_properties

class FDMDataEncoder(object):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
        
    def encode_fdm_data(self, fdm_properties):
        property_values = [self.fdmexec.get_property_value(fdm_property) for fdm_property in fdm_properties]
        
        fdm_data_string = struct.pack("!c" + "f" * len(property_values), chr(1), *property_values)
        
        return fdm_data_string

class FDMDataDecoder(object):
    def decode_fdm_data(self, datagram, fdm_properties):
        try:
            decoded_fdm_properties = struct.unpack("!c" + "f" * len(fdm_properties), datagram)
        except struct.error:
            raise ValueError("Invalid fdm datagram data")

        command_result = ord(decoded_fdm_properties[0])
        
        if command_result != 1:
            raise ValueError("Invalid fdm data command result code")
        
        decoded_fdm_properties = decoded_fdm_properties[1:]
        
        fdm_data = [(fdm_properties[index], fdm_property_value) for index, fdm_property_value in enumerate(decoded_fdm_properties)]
        return dict(fdm_data)

class FDMDataProtocol(DatagramProtocol):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
        self.fdm_data_encoder = FDMDataEncoder(fdmexec)
        
    def datagramReceived(self, datagram, (host, port)):
        try:
            decoded_packet = struct.unpack("!c", datagram)
        except struct.error:
            print("Failed to parse fdm data command datagram")
            logging.exception("Failed to parse fdm data command datagram")
            error_responce = struct.pack("!c", chr(255))
            self.transport.write(error_responce, (host, port))
            return
        
        command = ord(decoded_packet[0])
        if command == 1:
            encoded_fdm_data = self.fdm_data_encoder.encode_fdm_data(fdm_data_properties)
        
            self.transport.write(encoded_fdm_data, (host, port))
        else:
            print("Unknown fdm data command %d" % command)
            logging.error("Unknown fdm data command %d" % command)
            error_responce = struct.pack("!c", chr(255))
            self.transport.write(error_responce, (host, port))
    
class ControlsProtocol(DatagramProtocol):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
        self.fdm_data_decoder = FDMDataDecoder()
    
    def datagramReceived(self, datagram, addr):
        try:
            controls_data = self.fdm_data_decoder.decode_fdm_data(datagram, controls_properties)
        
            for control_property in controls_properties:
                self.fdmexec.set_property_value(control_property, controls_data[control_property])
        except ValueError:
            logging.error("Failed to parse control data")
            print("Failed to parse control data")

class FDMDataClientProtocol(DatagramProtocol):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.fdm_data_decoder = FDMDataDecoder()
    
    def startProtocol(self):
        fdm_data_command = struct.pack("!c", chr(1))
        self.transport.write(fdm_data_command, (self.host, self.port))
    
    def datagramReceived(self, datagram, addr):
        try:
            decoded_fdm_data = self.fdm_data_decoder.decode_fdm_data(datagram, fdm_data_properties)
            for fdm_property in fdm_data_properties:
                print("%s\t%f" % (fdm_property, decoded_fdm_data[fdm_property]))
        except ValueError:
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