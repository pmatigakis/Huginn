"""
The huginn.protocols module contains classes that are used by twisted in order
to transmit and receive simulation data.
"""

import struct
import logging
from abc import ABCMeta, abstractmethod

from twisted.internet.protocol import DatagramProtocol, Protocol, Factory
from twisted.protocols.basic import LineReceiver

class InvalidControlsDatagram(Exception):
    pass

class InvalidFDMDataRequestCommand(Exception):
    def __init__(self, command):
        Exception.__init__(self)
        self.command = command

class ControlsProtocol(DatagramProtocol):
    """The ControlsProtocol is used to receive and update tha aircraft's
    controls"""
    def __init__(self, aircraft):
        self.aircraft = aircraft

    def update_aircraft_controls(self, aileron, elevator, rudder, throttle):
        """Set the new aircraft controls values"""
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
    """The TelemetryProtocol is used to transmit telemetry data on a TCP
    connection"""
    def __init__(self, factory):
        self.factory = factory

        self.have_sent_header = False

        self.telemetry_items = [
            "time", "dt", "latitude", "longitude", "altitude",
            "airspeed", "heading", "x_acceleration", "y_acceleration",
            "z_acceleration", "roll_rate", "pitch_rate", "yaw_rate",
            "temperature", "static_pressure", "dynamic_pressure",
            "roll", "pitch", "thrust",
            "aileron", "elevator", "rudder", "throttle",
        ]

    def connectionMade(self):
        self.factory.clients.add(self)

    def connectionLost(self, reason):
        self.factory.clients.remove(self)

    def transmit_telemetry_data(self, telemetry_data):
        """Send the telemetry data"""
        if not self.have_sent_header:
            telemetry_header = ','.join(self.telemetry_items)
            telemetry_header += "\r\n"

            self.transport.write(telemetry_header)
            self.have_sent_header = True

        telemetry_string = ','.join([str(telemetry_data[value]) for value in self.telemetry_items])

        telemetry_string += "\r\n"

        self.transport.write(telemetry_string)

class TelemetryFactory(Factory):
    """The TelemetryFactory class is responsible for the creation of telemetry
    protocol clients"""
    def __init__(self, aircraft):
        self.aircraft = aircraft

        self.clients = set()

    def buildProtocol(self, addr):
        return TelemetryProtocol(self)

    def get_telemetry_data(self):
        return {
            "time": self.aircraft.fdmexec.GetSimTime(),
            "dt": self.aircraft.fdmexec.GetDeltaT(),
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
            "thrust": self.aircraft.engine.thrust,
            "aileron": self.aircraft.controls.aileron,
            "elevator": self.aircraft.controls.elevator,
            "rudder": self.aircraft.controls.rudder,
            "throttle": self.aircraft.engine.throttle,
        }

    def update_clients(self):
        """Send the telemetry data to the connected clients"""
        telemetry_data = self.get_telemetry_data()

        for client in self.clients:
            client.transmit_telemetry_data(telemetry_data)

class TelemetryDataListener(object):
    """The TelemetryDataListener class must be subclassed by any object that
    needs to be notified about the reception of telemetry data"""
    __metaclass__ = ABCMeta

    @abstractmethod
    def received_telemetry_header(self, header):
        pass

    @abstractmethod
    def received_telemetry_data(self, data):
        pass

class TelemetryClient(LineReceiver):
    """The TelemetryClient is used to receive telemetry data"""
    def __init__(self):
        self.header_received = False

    def lineReceived(self, line):
        data = line.strip().split(",")

        if self.header_received:
            self.factory.received_telemetry_data(data)
        else:
            self.header_received = True
            self.factory.received_telemetry_header(data)

class TelemetryClientFactory(Factory):
    """The TelemetryClientFactory is used to create a connection to the
    telemetry server"""
    def __init__(self):
        self.protocol = TelemetryClient
        self.listeners = []

    def add_telemetry_listener(self, listener):
        self.listeners.append(listener)

    def remove_telemetry_listener(self, listener):
        self.listeners.remove(listener)

    def received_telemetry_header(self, variable_names):
        """Called by the telemetry client when the telemetry header has been
        received"""
        for listener in self.listeners:
            listener.received_telemetry_header(variable_names)

    def received_telemetry_data(self, telemetry_data):
        """Called by the telemetry client when telemetry data have been
        received"""
        for listener in self.listeners:
            listener.received_telemetry_data(telemetry_data)

class FDMDataProtocol(DatagramProtocol):
    """The FDMDataProtocol class is used to transmit the flight dynamics model
    data to the client"""
    def __init__(self, aircraft, remote_host, port):
        self.aircraft = aircraft
        self.remote_host = remote_host
        self.port = port

    def get_fdm_data(self):
        fdm_data = [
            self.aircraft.fdmexec.GetSimTime(),
            self.aircraft.gps.latitude,
            self.aircraft.gps.longitude,
            self.aircraft.gps.altitude,
            self.aircraft.gps.airspeed,
            self.aircraft.gps.heading,
            self.aircraft.accelerometer.x_acceleration,
            self.aircraft.accelerometer.y_acceleration,
            self.aircraft.accelerometer.z_acceleration,
            self.aircraft.gyroscope.roll_rate,
            self.aircraft.gyroscope.pitch_rate,
            self.aircraft.gyroscope.yaw_rate,
            self.aircraft.thermometer.temperature,
            self.aircraft.pressure_sensor.pressure,
            self.aircraft.pitot_tube.pressure,
            self.aircraft.inertial_navigation_system.roll,
            self.aircraft.inertial_navigation_system.pitch,
            self.aircraft.engine.thrust,
            self.aircraft.controls.aileron,
            self.aircraft.controls.elevator,
            self.aircraft.controls.rudder,
            self.aircraft.engine.throttle,
        ]

        return fdm_data

    def send_fdm_data(self):
        fdm_data = self.get_fdm_data()

        datagram = struct.pack("f" * len(fdm_data),
                               *fdm_data)

        self.transport.write(datagram, (self.remote_host, self.port))

class FDMDataListener(object):
    """The methods of the FDMDataListener class must be implemented by any
    object that wants to handle the fdm data received from Huginn"""
    __metaclass = ABCMeta

    @abstractmethod
    def fdm_data_received(self, fdm_data):
        pass

class FDMDataClient(DatagramProtocol):
    """The FDMDataClient is used to receive fdm data from Huginn"""
    def __init__(self):
        self.listeners = []

    def add_fdm_data_listener(self, listener):
        self.listeners.append(listener)

    def remove_fdm_data_listener(self, listener):
        self.listeners.remove(listener)

    def _notify_fdm_data_listeners(self, fdm_data):
        for fdm_data_listener in self.listeners:
            fdm_data_listener.fdm_data_received(fdm_data)

    def datagramReceived(self, datagram, addr):
        fdm_data = decode_fdm_data_datagram(datagram)

        self._notify_fdm_data_listeners(fdm_data)

class ControlsClient(DatagramProtocol):
    """The ControlsClient is used to transmit the updated aircraft controls
    to Huginn"""
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def startProtocol(self):
        self.transport.connect(self.host, self.port)

    def send_datagram(self, datagram):
        self.transport.write(datagram)

    def transmit_controls(self, aileron, elevator, rudder, throttle):
        """Send the aircraft controls to Huginn"""
        controls_datagram = struct.pack("!ffff",
                                        aileron,
                                        elevator,
                                        rudder,
                                        throttle)

        self.send_datagram(controls_datagram)

def decode_fdm_data_datagram(datagram):
    """Decode a datagram packet that contains the fdm data"""
    data = struct.unpack("f" * 22, datagram)

    fdm_data = {
        "time": data[0],
        "latitude": data[1],
        "longitude": data[2],
        "altitude": data[3],
        "airspeed": data[4],
        "heading": data[5],
        "x_acceleration": data[6],
        "y_acceleration": data[7],
        "z_acceleration": data[8],
        "roll_rate": data[9],
        "pitch_rate": data[10],
        "yaw_rate": data[11],
        "temperature": data[12],
        "static_pressure": data[13],
        "total_pressure": data[14],
        "roll": data[15],
        "pitch": data[16],
        "thrust": data[17],
        "aileron": data[18],
        "elevator": data[19],
        "rudder": data[20],
        "throttle": data[21]
    }

    return fdm_data
