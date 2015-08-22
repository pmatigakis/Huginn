import struct
import logging

from twisted.internet.protocol import DatagramProtocol
from twisted.protocols.policies import TimeoutMixin
from twisted.internet import reactor

from huginn.fdm import controls_properties

ACCELEROMETER_DATA = 0x01
GYROSCOPE_DATA = 0x02
MAGNETOMETER_DATA = 0x04
GPS_DATA = 0x08
ATMOSPHERIC_PRESSURE_DATA = 0x10
TEMPERATURE_DATA = 0x20

ERROR_COMMAND = 0x80

FDM_DATA_PROTOCOL_PROPERTIES = {
    ACCELEROMETER_DATA: [
        "accelerations/a-pilot-x-ft_sec2",
        "accelerations/a-pilot-y-ft_sec2",
        "accelerations/a-pilot-z-ft_sec2"
    ],
                                
    GYROSCOPE_DATA: [
        "velocities/p-rad_sec",
        "velocities/q-rad_sec",
        "velocities/r-rad_sec"
    ],
                                
    MAGNETOMETER_DATA: [
    ],
                                
    GPS_DATA: [
        "position/lat-gc-deg",
        "position/long-gc-deg",
        "position/h-sl-ft",
        "velocities/vtrue-kts",
        "attitude/heading-true-rad"
    ],
                                
    ATMOSPHERIC_PRESSURE_DATA: [
        "atmosphere/P-psf",
        "aero/qbar-psf"
    ],
                                
    TEMPERATURE_DATA: [
        "atmosphere/T-R"
    ]
}

class InvalidFDMDataCommandDatagram(Exception):
    pass

class InvalidFDMDataRequestCommand(Exception):
    def __init__(self, command):
        self.command = command

class InvalidFDMDataResponceDatagram(Exception):
    def __init__(self, datagram):
        self.datagram = datagram

class FDMDataRequest(object):
    def __init__(self, host, port, command):
        self.host = host
        self.port = port
        self.command = command

    def __eq__(self, other):
        if not isinstance(other, FDMDataRequest):
            return False
        
        if self.host != other.host:
            return False
        elif self.port != other.port:
            return False
        elif self.command != other.command:
            return False
        
        return True

class FDMDataResponse(object):
    def __init__(self, fdm_data_request, fdm_property_values):
        self.fdm_data_request = fdm_data_request
        self.fdm_property_values = fdm_property_values

    def __eq__(self, other):
        if not isinstance(other, FDMDataResponse):
            return False
        
        if self.fdm_data_request != other.fdm_data_request:
            return False
        elif self.fdm_property_values != other.fdm_property_values:
            return False
        
        return True

class FDMDataResponceDecoder(object):
    def decode_responce(self, datagram):
        if len(datagram) < 1:
            raise ValueError("The fdm data datagram does not contain any data")
        
        command, data = datagram[0], datagram[1:]
        command = ord(command)
        
        fdm_properties = []
        
        if not command & ERROR_COMMAND:
            property_flags = sorted(FDM_DATA_PROTOCOL_PROPERTIES.keys(), reverse=True)
            
            for property_flag in property_flags:
                if command & property_flag:
                    fdm_properties.extend(FDM_DATA_PROTOCOL_PROPERTIES[property_flag]) 
        else:
            return command, {}
        
        try:
            decoded_fdm_properties = struct.unpack("!" + ("f" * len(fdm_properties)), data)
        except struct.error:
            raise ValueError("Invalid fdm datagram data")
        
        fdm_data = [(fdm_properties[index], fdm_property_value) for index, fdm_property_value in enumerate(decoded_fdm_properties)]
        return command, dict(fdm_data)

class FDMDataProtocol(DatagramProtocol):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
    
    def decode_request(self, datagram, host, port):
        try:
            command = struct.unpack("!c", datagram)
            command = ord(command[0]) & 0x3f
        except:
            raise InvalidFDMDataCommandDatagram()
                
        return FDMDataRequest(host, port, command)
    
    def process_request(self, request):
        property_flags = sorted(FDM_DATA_PROTOCOL_PROPERTIES.keys(), reverse=True)
        
        fdm_properties = []
        
        for property_flag in property_flags:
            if request.command & property_flag:
                fdm_properties.extend(FDM_DATA_PROTOCOL_PROPERTIES[property_flag])
        
        fdm_property_values = [self.fdmexec.get_property_value(fdm_property) for fdm_property in fdm_properties]
        response = FDMDataResponse(request, fdm_property_values)
            
        self.send_response(response)
    
    def encode_response(self, response):
        fdm_property_values_count = len(response.fdm_property_values)
        
        encoded_response = struct.pack("!c" + ("f" * fdm_property_values_count), chr(response.fdm_data_request.command), *response.fdm_property_values)

        return encoded_response
            
    def send_response(self, response):
        encoded_response = self.encode_response(response)
        
        remote_host = response.fdm_data_request.host
        remote_port = response.fdm_data_request.port
        
        self.transmit_datagram(encoded_response, remote_host, remote_port)
    
    def transmit_datagram(self, datagram, host, port):
        self.transport.write(datagram, (host, port))
    
    def datagramReceived(self, datagram, address):
        host, port = address
        
        try:
            request = self.decode_request(datagram, host, port)
        except InvalidFDMDataCommandDatagram:
            print("Failed to parse fdm data command datagram")
            logging.exception("Failed to parse fdm data command datagram")
            error_response = struct.pack("!c", chr(255))
            self.transmit_datagram(error_response, (host, port))
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

class FDMDataClientProtocol(DatagramProtocol, TimeoutMixin):
    def __init__(self, host, port):
        self.host = host
        self.port = port
    
    def startProtocol(self):
        fdm_data_command = struct.pack("!c", chr(0x3f)) #get all fdm data
        self.transport.write(fdm_data_command, (self.host, self.port))
        self.setTimeout(0.01)
    
    def datagramReceived(self, datagram, addr):
        self.resetTimeout()
        
        fdm_data_decoder = FDMDataResponceDecoder()
        
        try:
            command, decoded_fdm_data = fdm_data_decoder.decode_responce(datagram)
        except ValueError:
            print("Failed to parse received data")
        
        property_flags = sorted(FDM_DATA_PROTOCOL_PROPERTIES.keys(), reverse=True)
        
        for fdm_property in sorted(decoded_fdm_data.keys()):
            print("%s\t%f" % (fdm_property, decoded_fdm_data[fdm_property]))
            
        reactor.stop()
    
    def timeoutConnection(self):
        print("The fdm server did not respond in time")
        reactor.stop()
    
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
        
        reactor.stop()