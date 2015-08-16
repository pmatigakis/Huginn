import struct
import logging

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

from huginn.fdm import fdm_data_properties, controls_properties

class InvalidFDMDataCommandDatagram(Exception):
    pass

class InvalidFDMDataRequestCommand(Exception):
    def __init__(self, command):
        self.command = command

class InvalidFDMDataResponceDatagram(Exception):
    def __init__(self, datagram):
        self.datagram = datagram

def decode_fdm_data_command(self, datagram):
        command = struct.unpack("!c", datagram[0])
        command = ord(command[0])
        
        if command == 1:
            pass
        else:
            raise InvalidFDMDataCommandDatagram()

class FDMDataRequest(object):
    def __init__(self, host, port, command, fdm_properties):
        self.host = host
        self.port = port
        self.command = command
        self.fdm_properties = fdm_properties

    def __eq__(self, other):
        if not isinstance(other, FDMDataRequest):
            return False
        
        if self.host != other.host:
            return False
        elif self.port != other.port:
            return False
        elif self.command != other.command:
            return False
        elif self.fdm_properties != other.fdm_properties:
            return False
        
        return True

class FDMDataResponce(object):
    def __init__(self, fdm_data_request, fdm_property_values):
        self.fdm_data_request = fdm_data_request
        self.fdm_property_values = fdm_property_values

    def __eq__(self, other):
        if not isinstance(other, FDMDataResponce):
            return False
        
        if self.fdm_data_request != other.fdm_data_request:
            return False
        elif self.fdm_property_values != other.fdm_property_values:
            return False
        
        return True

class FDMDataResponceDecoder(object):
    def decode_responce(self, datagram):
        try:
            decoded_fdm_properties = struct.unpack("!c" + "f" * len(fdm_data_properties), datagram)
        except struct.error:
            raise ValueError("Invalid fdm datagram data")
        
        command = ord(decoded_fdm_properties[0]) 
        
        if command != 1:
            raise InvalidFDMDataResponceDatagram(datagram)
        
        decoded_fdm_properties = decoded_fdm_properties[1:]
        
        fdm_data = [(fdm_data_properties[index], fdm_property_value) for index, fdm_property_value in enumerate(decoded_fdm_properties)]
        return dict(fdm_data)

class FDMDataProtocol(DatagramProtocol):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
    
    def decode_request(self, datagram, host, port):
        datagram_size = len(datagram)
        if datagram_size <= 0:
            raise InvalidFDMDataCommandDatagram()
        
        command = struct.unpack("!c", datagram)
        command = ord(command[0])
        
        if command == 1 and datagram_size == 1:
            return FDMDataRequest(host, port, command, fdm_data_properties)
        else:
            raise InvalidFDMDataCommandDatagram()
    
    def process_request(self, request):
        if request.command == 1:
            fdm_property_values = [self.fdmexec.get_property_value(fdm_property) for fdm_property in fdm_data_properties]
            responce = FDMDataResponce(request, fdm_property_values)
            
            self.send_responce(responce)
        else:
            print("Unknown fdm data request command %" % request.command)
            logging.error("Unknown fdm data request command %" % request.command)
            error_responce = struct.pack("!c", chr(255))
            self.transport.write(error_responce, (request.host, request.port))
    
    def encode_responce(self, responce):
        command = responce.fdm_data_request.command
        
        if command == 1:
            fdm_property_values_count = len(responce.fdm_property_values)
            encoded_responce = struct.pack("!c" + ("f" * fdm_property_values_count), chr(1), *responce.fdm_property_values)
            
            return encoded_responce
        else:
            raise InvalidFDMDataRequestCommand(command)
    
    def send_responce(self, responce):
        try:
            encoded_responce = self.encode_responce(responce)
        except InvalidFDMDataRequestCommand as e:
            print("Invalid fdm data request command %d" % e.command)
            logging.exception("Invalid fdm data request command %d" % e.command)
            return
        
        remote_host = responce.fdm_data_request.host
        remote_port = responce.fdm_data_request.port
        
        self.transport.write(encoded_responce, (remote_host, remote_port))
    
    def datagramReceived(self, datagram, address):
        host, port = address
        
        try:
            request = self.decode_request(datagram, host, port)
        except InvalidFDMDataCommandDatagram:
            print("Failed to parse fdm data command datagram")
            logging.exception("Failed to parse fdm data command datagram")
            error_responce = struct.pack("!c", chr(255))
            self.transport.write(error_responce, (host, port))
            return
        
        self.process_request(request)
    
class ControlsProtocol(DatagramProtocol):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
    
    def datagramReceived(self, datagram, addr):
        try:
            controls_data = struct.unpack("!" + ("f" % len(controls_properties)), datagram)
        
            for control_property in controls_properties:
                self.fdmexec.set_property_value(control_property, controls_data[control_property])
        except ValueError:
            logging.error("Failed to parse control data")
            print("Failed to parse control data")

class FDMDataClientProtocol(DatagramProtocol):
    def __init__(self, host, port):
        self.host = host
        self.port = port
    
    def startProtocol(self):
        fdm_data_command = struct.pack("!c", chr(1))
        self.transport.write(fdm_data_command, (self.host, self.port))
    
    def datagramReceived(self, datagram, addr):
        fdm_data_decoder = FDMDataResponceDecoder()
        
        try:
            decoded_fdm_data = fdm_data_decoder.decode_responce(datagram)
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