import struct
import logging

from twisted.internet.protocol import DatagramProtocol
from twisted.protocols.policies import TimeoutMixin
from twisted.internet import reactor

from huginn.fdm import controls_properties

FDM_DATA_COMMAND = 0x01
ERROR_CODE = 0xff

FDM_DATA_RESPONCE_OK = 0x01

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

    def encode_response(self):
        fdm_property_values_count = len(self.fdm_property_values)
        
        encoded_response = struct.pack("!c" + ("f" * fdm_property_values_count), chr(FDM_DATA_RESPONCE_OK), *self.fdm_property_values)

        return encoded_response

    def __eq__(self, other):
        if not isinstance(other, FDMDataResponse):
            return False
        
        if self.fdm_data_request != other.fdm_data_request:
            return False
        elif self.fdm_property_values != other.fdm_property_values:
            return False
        
        return True

class FDMDataResponseDecoder(object):
    def decode_response(self, datagram):
        if len(datagram) < 1:
            raise ValueError("The fdm data datagram does not contain any data")
        
        command, data = datagram[0], datagram[1:]
        command = ord(command)
        
        if command & FDM_DATA_RESPONCE_OK:
            try:
                decoded_fdm_properties = struct.unpack("!" + ("f" * 14), data)
                
                fdm_data = {
                    "temperature": decoded_fdm_properties[0],
                    "dynamic_pressure": decoded_fdm_properties[1],
                    "static_pressure": decoded_fdm_properties[2],
                    "latitude": decoded_fdm_properties[3],
                    "longitude": decoded_fdm_properties[4],
                    "altitude": decoded_fdm_properties[5],
                    "airspeed": decoded_fdm_properties[6],
                    "heading": decoded_fdm_properties[7],
                    "x_aceleration": decoded_fdm_properties[8],
                    "y_aceleration": decoded_fdm_properties[9],
                    "z_aceleration": decoded_fdm_properties[10],
                    "roll_rate": decoded_fdm_properties[11],
                    "pitch_rate": decoded_fdm_properties[12],
                    "yaw_rate": decoded_fdm_properties[13],
                }
                
                return command, fdm_data
            except struct.error:
                raise ValueError("Invalid fdm datagram data")
        else:
            return command, {}
        
class FDMDataProtocol(DatagramProtocol):
    def __init__(self, aircraft):
        self.aircraft = aircraft
    
    def decode_request(self, datagram, host, port):
        try:
            command = struct.unpack("!c", datagram)
        except:
            raise InvalidFDMDataCommandDatagram()
                
        command = ord(command[0])
        return FDMDataRequest(host, port, command)
    
    def create_fdm_data_responce(self, request):
        fdm_property_values = []
        
        fdm_property_values.append(self.aircraft.thermometer.temperature)
        fdm_property_values.append(self.aircraft.pitot_tube.pressure)
        fdm_property_values.append(self.aircraft.pressure_sensor.pressure)
        fdm_property_values.append(self.aircraft.gps.latitude)
        fdm_property_values.append(self.aircraft.gps.longitude)
        fdm_property_values.append(self.aircraft.gps.altitude)
        fdm_property_values.append(self.aircraft.gps.airspeed)
        fdm_property_values.append(self.aircraft.gps.heading)
        fdm_property_values.append(self.aircraft.accelerometer.x_acceleration)
        fdm_property_values.append(self.aircraft.accelerometer.y_acceleration)
        fdm_property_values.append(self.aircraft.accelerometer.z_acceleration)
        fdm_property_values.append(self.aircraft.gyroscope.roll_rate)
        fdm_property_values.append(self.aircraft.gyroscope.pitch_rate)
        fdm_property_values.append(self.aircraft.gyroscope.yaw_rate)
        
        response = FDMDataResponse(request, fdm_property_values)
        
        return response
    
    def process_request(self, request):
        if request.command == FDM_DATA_COMMAND:
            response = self.create_fdm_data_responce(request)
        else:
            raise InvalidFDMDataRequestCommand(request.command)
        
        self.send_response(response)
                
    def send_response(self, response):        
        remote_host = response.fdm_data_request.host
        remote_port = response.fdm_data_request.port
        
        self.transmit_datagram(response.encode_response(), remote_host, remote_port)
    
    def transmit_datagram(self, datagram, host, port):
        self.transport.write(datagram, (host, port))
    
    def transmit_error_code(self, error_code, host, port):
        error_response = struct.pack("!c", chr(error_code))
        self.transmit_datagram(error_response, host, port)
                
    def datagramReceived(self, datagram, address):
        host, port = address
        
        try:
            request = self.decode_request(datagram, host, port)
            
            self.process_request(request)
        except InvalidFDMDataCommandDatagram:
            print("Failed to parse fdm data command datagram")
            logging.exception("Failed to parse fdm data command datagram")
            self.transmit_error_code(ERROR_CODE, host, port)
        except InvalidFDMDataRequestCommand:
            print("Invalid fdm data command")
            logging.exception("Invalid fdm data command")
            self.transmit_error_code(ERROR_CODE, host, port)
    
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
        fdm_data_command = struct.pack("!c", chr(FDM_DATA_COMMAND))
        self.transport.write(fdm_data_command, (self.host, self.port))
        self.setTimeout(0.01)
    
    def datagramReceived(self, datagram, addr):
        self.resetTimeout()
        
        fdm_data_decoder = FDMDataResponseDecoder()
        
        try:
            command, decoded_fdm_data = fdm_data_decoder.decode_response(datagram)
        except ValueError:
            print("Failed to parse received data")
        
        if command == FDM_DATA_COMMAND:
            for fdm_property in decoded_fdm_data.keys():
                print("%s\t%f" % (fdm_property, decoded_fdm_data[fdm_property]))
        else:
            print("Invalid response")
            
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