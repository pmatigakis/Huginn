import struct
import logging

from twisted.internet.protocol import DatagramProtocol, Protocol, Factory
from twisted.internet import reactor
from twisted.protocols.basic import LineReceiver

#Declare the available commands supported by the fdm data protocol
GPS_DATA_REQUEST = 0x00
ACCELEROMETER_DATA_REQUEST = 0x01
GYROSCOPE_DATA_REQUEST = 0x02
MAGNETOMETER_DATA_REQUEST = 0x03
THERMOMETER_DATA_REQUEST = 0x04
PITOT_TUBE_DATA_REQUEST = 0x05
STATIC_PRESSURE_DATA_REQUEST = 0x06
INS_DATA_REQUEST = 0x07

#fdm data request response codes
ERROR_CODE = 0xff
FDM_DATA_RESPONCE_OK = 0x00

#Simulator control request codes
SIMULATION_RESUME = 0x00
SIMULATION_PAUSE = 0x01
SIMULATION_RESET = 0x02
SIMULATION_STATUS = 0x03

class InvalidControlsDatagram(Exception):
    pass

class InvalidFDMDataRequestDatagram(Exception):
    pass

class InvalidFDMDataRequestCommand(Exception):
    def __init__(self, command):
        Exception.__init__(self)
        self.command = command

class InvalidFDMDataResponceDatagram(Exception):
    def __init__(self, datagram):
        Exception.__init__(self)
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

        encoded_response = struct.pack("!cc" + ("f" * fdm_property_values_count), chr(FDM_DATA_RESPONCE_OK),
                                                                                  chr(self.fdm_data_request.command),
                                                                                  *self.fdm_property_values)

        return encoded_response

    def __eq__(self, other):
        if not isinstance(other, FDMDataResponse):
            return False

        if self.fdm_data_request != other.fdm_data_request:
            return False
        elif self.fdm_property_values != other.fdm_property_values:
            return False

        return True

class FDMDataProtocol(DatagramProtocol):
    def __init__(self, aircraft):
        self.aircraft = aircraft

        self.request_processors = {
            GPS_DATA_REQUEST: self.create_gps_data_response,
            ACCELEROMETER_DATA_REQUEST: self.create_accelerometer_data_response,
            GYROSCOPE_DATA_REQUEST: self.create_gyroscope_data_response,
            MAGNETOMETER_DATA_REQUEST: self.create_magnetometer_data_response,
            PITOT_TUBE_DATA_REQUEST: self.create_pitot_tube_data_response,
            STATIC_PRESSURE_DATA_REQUEST: self.create_static_pressure_data_response,
            THERMOMETER_DATA_REQUEST: self.create_thermometer_data_response,
            INS_DATA_REQUEST: self.create_ins_data_response
        }

    def decode_request(self, datagram, host, port):
        try:
            command = struct.unpack("!c", datagram)
        except:
            raise InvalidFDMDataRequestDatagram()

        command = ord(command[0])
        return FDMDataRequest(host, port, command)

    def create_gps_data_response(self, request):
        gps_values = [
            self.aircraft.gps.latitude,
            self.aircraft.gps.longitude,
            self.aircraft.gps.altitude,
            self.aircraft.gps.airspeed,
            self.aircraft.gps.heading
        ]

        return FDMDataResponse(request, gps_values)

    def create_accelerometer_data_response(self, request):
        accelerometer_values = [
            self.aircraft.accelerometer.x_acceleration,
            self.aircraft.accelerometer.y_acceleration,
            self.aircraft.accelerometer.z_acceleration
        ]

        return FDMDataResponse(request, accelerometer_values)

    def create_gyroscope_data_response(self, request):
        gyroscope_data = [
            self.aircraft.gyroscope.roll_rate,
            self.aircraft.gyroscope.pitch_rate,
            self.aircraft.gyroscope.yaw_rate
        ]

        return FDMDataResponse(request, gyroscope_data)

    def create_magnetometer_data_response(self, request):
        return FDMDataResponse(request, [0.0, 0.0, 0.0])

    def create_thermometer_data_response(self, request):
        return FDMDataResponse(request,
                               [self.aircraft.thermometer.temperature])

    def create_pitot_tube_data_response(self, request):
        return FDMDataResponse(request, [self.aircraft.pitot_tube.pressure])

    def create_static_pressure_data_response(self, request):
        return FDMDataResponse(request,
                               [self.aircraft.pressure_sensor.pressure])

    def create_ins_data_response(self, request):
        ins_data = [
            self.aircraft.inertial_navigation_system.roll,
            self.aircraft.inertial_navigation_system.pitch,
            self.aircraft.inertial_navigation_system.heading,
            self.aircraft.inertial_navigation_system.latitude,
            self.aircraft.inertial_navigation_system.longitude,
            self.aircraft.inertial_navigation_system.airspeed,
            self.aircraft.inertial_navigation_system.altitude,
        ]

        return FDMDataResponse(request, ins_data)

    def get_request_processor(self, command):
        return self.request_processors.get(command, None)

    def create_response(self, request):
        command = request.command

        request_processor = self.get_request_processor(command)

        if not request_processor:
            raise InvalidFDMDataRequestCommand(request.command)

        response = request_processor(request)

        return response

    def process_request(self, request):
        response = self.create_response(request)

        self.send_response(response)

    def send_response(self, response):
        remote_host = response.fdm_data_request.host
        remote_port = response.fdm_data_request.port

        self.transmit_datagram(response.encode_response(),
                               remote_host,
                               remote_port)

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
        except InvalidFDMDataRequestDatagram:
            print("Failed to parse fdm data command datagram")
            logging.error("Failed to parse fdm data command datagram")
            self.transmit_error_code(ERROR_CODE, host, port)
        except InvalidFDMDataRequestCommand:
            print("Invalid fdm data command")
            logging.error("Invalid fdm data command")
            self.transmit_error_code(ERROR_CODE, host, port)

class ControlsProtocol(DatagramProtocol):
    def __init__(self, aircraft):
        self.aircraft = aircraft

    def update_aircraft_controls(self, aileron, elevator, rudder, throttle):
        self.aircraft.controls.aileron = aileron
        self.aircraft.controls.elevator = elevator
        self.aircraft.controls.rudder = rudder
        self.aircraft.controls.throttle = throttle

    def decode_datagram(self, datagram):
        try:
            controls_data = struct.unpack("!ffff", datagram)

            return controls_data
        except ValueError:
            raise InvalidControlsDatagram()

    def datagramReceived(self, datagram, addr):
        try:
            controls = self.decode_datagram(datagram)
        except InvalidControlsDatagram:
            logging.error("Failed to parse control data")
            print("Failed to parse control data")
            return

        aileron = controls[0]
        elevator = controls[1]
        rudder = controls[2]
        throttle = controls[3]

        self.update_aircraft_controls(aileron, elevator, rudder, throttle)

class TelemetryProtocol(Protocol):
    def __init__(self, factory):
        self.factory = factory

        self.have_sent_header = False

        self.telemetry_items = [
            "time", "dt", "latitude", "longitude", "altitude",
            "airspeed", "heading", "x_acceleration", "y_acceleration",
            "z_acceleration", "roll_rate", "pitch_rate", "yaw_rate",
            "temperature", "static_pressure", "dynamic_pressure",
            "roll", "pitch", "engine_rpm", "engine_thrust",
            "engine_power", "aileron", "elevator", "rudder", "throttle",
        ]

    def connectionMade(self):
        self.factory.clients.add(self)

    def connectionLost(self, reason):
        self.factory.clients.remove(self)

    def transmit_telemetry_data(self, telemetry_data):
        if not self.have_sent_header:
            telemetry_header = ','.join(self.telemetry_items)
            telemetry_header += "\r\n"
            
            self.transport.write(telemetry_header)
            self.have_sent_header = True

        telemetry_string = ','.join([str(telemetry_data[value]) for value in self.telemetry_items])
        
        telemetry_string += "\r\n"
        
        self.transport.write(telemetry_string)

class TelemetryFactory(Factory):
    def __init__(self, fdm_model, aircraft):
        self.fdm_model = fdm_model
        self.aircraft = aircraft

        self.clients = set()

    def buildProtocol(self, addr):
        return TelemetryProtocol(self)

    def get_telemetry_data(self):
        return {
            "time": self.fdm_model.get_property_value("simulation/sim-time-sec"),
            "dt": self.fdm_model.get_property_value("simulation/dt"),
            "latitude": self.aircraft.gps.latitude,
            "longitude": self.aircraft.gps.longitude,
            "altitude": self.aircraft.gps.altitude,
            "airspeed": self.aircraft.gps.airspeed,
            "heading": self.aircraft.gps.heading,
            "x_acceleration": self.aircraft.accelerometer.x_acceleration,
            "y_acceleration": self.aircraft.accelerometer.y_acceleration,
            "z_acceleration": self.aircraft.accelerometer.z_acceleration,
            "roll_rate": self.aircraft.gyroscope.roll_rate,
            "pitch_rate": self.aircraft.gyroscope.pitch_rate,
            "yaw_rate": self.aircraft.gyroscope.yaw_rate,
            "temperature": self.aircraft.thermometer.temperature,
            "static_pressure": self.aircraft.pressure_sensor.pressure,
            "dynamic_pressure": self.aircraft.pitot_tube.pressure,
            "roll": self.aircraft.inertial_navigation_system.roll,
            "pitch": self.aircraft.inertial_navigation_system.pitch,
            "engine_rpm": self.aircraft.engine.rpm,
            "engine_thrust": self.aircraft.engine.thrust,
            "engine_power": self.aircraft.engine.power,
            "aileron": self.aircraft.controls.aileron,
            "elevator": self.aircraft.controls.elevator,
            "rudder": self.aircraft.controls.rudder,
            "throttle": self.aircraft.engine.throttle,
        }

    def update_clients(self):
        telemetry_data = self.get_telemetry_data()
    
        for client in self.clients:
            client.transmit_telemetry_data(telemetry_data)

class TelemetryClient(LineReceiver):
    def __init__(self, output_file):
        self.output_file = output_file

    def lineReceived(self, line):
        self.output_file.write(line + "\n")

class TelemetryClientFactory(Factory):
    def __init__(self, output_file):
        self.output_file = output_file

    def buildProtocol(self, addr):
        return TelemetryClient(self.output_file)
