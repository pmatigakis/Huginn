"""
The huginn.protocols module contains classes that are used by twisted in order
to transmit and receive simulation data.
"""

import logging
from abc import ABCMeta, abstractmethod

from twisted.internet.protocol import DatagramProtocol, Factory
from twisted.protocols.basic import Int32StringReceiver
from google.protobuf.message import DecodeError

from huginn import fdm_pb2

class ControlsProtocol(DatagramProtocol):
    """The ControlsProtocol is used to receive and update tha aircraft's
    controls"""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
        self.logger = logging.getLogger("huginn")

    def update_aircraft_controls(self, aileron, elevator, rudder, throttle):
        """Set the new aircraft controls values"""
        if aileron > 1.0:
            aileron = 1.0
        elif aileron < -1.0:
            aileron = -1.0

        self.fdmexec.GetFCS().SetDaCmd(aileron)

        if elevator > 1.0:
            elevator = 1.0
        elif elevator < -1.0:
            elevator = -1.0

        self.fdmexec.GetFCS().SetDeCmd(elevator)

        if rudder > 1.0:
            rudder = 1.0
        elif rudder < -1.0:
            rudder = -1.0

        self.fdmexec.GetFCS().SetDrCmd(rudder)

        if throttle > 1.0:
            throttle = 1.0
        elif throttle < 0.0:
            throttle = 0.0

        for i in range(self.fdmexec.GetPropulsion().GetNumEngines()):
            self.fdmexec.GetFCS().SetThrottleCmd(i, throttle)

    def datagramReceived(self, datagram, addr):
        controls = fdm_pb2.Controls()

        try:
            controls.ParseFromString(datagram)
        except DecodeError:
            logging.exception("Failed to parse control data")
            print("Failed to parse control data")
            return

        self.update_aircraft_controls(controls.aileron,
                                      controls.elevator,
                                      controls.rudder,
                                      controls.throttle)

class FDMDataProtocol(DatagramProtocol):
    """The FDMDataProtocol class is used to transmit the flight dynamics model
    data to the client"""
    def __init__(self, fdmexec, aircraft, remote_host, port):
        self.fdmexec = fdmexec
        self.aircraft = aircraft
        self.remote_host = remote_host
        self.port = port

    def get_fdm_data(self):
        """Return the fdm data"""
        fdm_data = fdm_pb2.FDMData()

        fdm_data.time = self.fdmexec.GetSimTime()

        fdm_data.gps.latitude = self.aircraft.instruments.gps.latitude
        fdm_data.gps.longitude = self.aircraft.instruments.gps.longitude
        fdm_data.gps.altitude = self.aircraft.instruments.gps.altitude
        fdm_data.gps.airspeed = self.aircraft.instruments.gps.airspeed
        fdm_data.gps.heading = self.aircraft.instruments.gps.heading

        fdm_data.accelerometer.x_acceleration = self.aircraft.sensors.accelerometer.x
        fdm_data.accelerometer.y_acceleration = self.aircraft.sensors.accelerometer.y
        fdm_data.accelerometer.z_acceleration = self.aircraft.sensors.accelerometer.z

        fdm_data.gyroscope.roll_rate = self.aircraft.gyroscope.roll_rate
        fdm_data.gyroscope.pitch_rate = self.aircraft.gyroscope.pitch_rate
        fdm_data.gyroscope.yaw_rate = self.aircraft.gyroscope.yaw_rate

        fdm_data.thermometer.temperature = self.aircraft.thermometer.temperature

        fdm_data.pressure_sensor.pressure = self.aircraft.pressure_sensor.pressure
        fdm_data.pitot_tube.pressure = self.aircraft.pitot_tube.pressure

        fdm_data.engine.thrust = self.aircraft.engine.thrust
        fdm_data.engine.throttle = self.aircraft.engine.throttle

        fdm_data.controls.aileron = self.aircraft.controls.aileron
        fdm_data.controls.elevator = self.aircraft.controls.elevator
        fdm_data.controls.rudder = self.aircraft.controls.rudder
        fdm_data.controls.throttle = self.aircraft.controls.throttle

        fdm_data.ins.roll = self.aircraft.inertial_navigation_system.roll
        fdm_data.ins.pitch = self.aircraft.inertial_navigation_system.pitch

        return fdm_data

    def send_fdm_data(self):
        """Transmit the fdm data"""
        fdm_data = self.get_fdm_data()

        datagram = fdm_data.SerializeToString()

        self.transport.write(datagram, (self.remote_host, self.port))

class FDMDataListener(object):
    """The methods of the FDMDataListener class must be implemented by any
    object that wants to handle the fdm data received from Huginn"""
    __metaclass = ABCMeta

    @abstractmethod
    def fdm_data_received(self, fdm_data):
        """This function is called when fdm data have been received so that
        the implementing class can handler them

        Arguments:
        fdm_data: a protocol buffer object that contains the fdm data
        """
        pass

class FDMDataClient(DatagramProtocol):
    """The FDMDataClient is used to receive fdm data from Huginn"""
    def __init__(self):
        self.listeners = []

    def add_fdm_data_listener(self, listener):
        """Add an fdm data listener"""
        self.listeners.append(listener)

    def remove_fdm_data_listener(self, listener):
        """Remove an fdm data listener"""
        self.listeners.remove(listener)

    def _notify_fdm_data_listeners(self, fdm_data):
        """Update the fdm data listeners

        Arguments:
        fdm_data: a protocol buffer object that contains the fdm data
        """
        for fdm_data_listener in self.listeners:
            fdm_data_listener.fdm_data_received(fdm_data)

    def datagramReceived(self, datagram, addr):
        fdm_data = fdm_pb2.FDMData()

        fdm_data.ParseFromString(datagram)

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
        """Transmit the UDP datagram that contains the aircraft controls
        values

        Arguments:
        datagram: that datagram to transmit
        """
        self.transport.write(datagram)

    def transmit_controls(self, aileron, elevator, rudder, throttle):
        """Send the aircraft controls to Huginn"""
        controls = fdm_pb2.Controls()
        controls.aileron = aileron
        controls.elevator = elevator
        controls.rudder = rudder
        controls.throttle = throttle

        self.send_datagram(controls.SerializeToString())

class SensorDataProtocol(Int32StringReceiver):
    """The SensorDataProtocol is used to transmit the aircraft's sensor data"""
    def fill_gps_data(self, sensor_data_response):
        sensor_data_response.type = fdm_pb2.GPS_REQUEST

        sensor_data_response.gps.latitude = self.factory.aircraft.instruments.gps.latitude
        sensor_data_response.gps.longitude = self.factory.aircraft.instruments.gps.longitude
        sensor_data_response.gps.altitude = self.factory.aircraft.instruments.gps.altitude
        sensor_data_response.gps.airspeed = self.factory.aircraft.instruments.gps.airspeed
        sensor_data_response.gps.heading = self.factory.aircraft.instruments.gps.heading

    def fill_accelerometer_data(self, sensor_data_response):
        sensor_data_response.type = fdm_pb2.ACCELEROMETER_REQUEST

        sensor_data_response.accelerometer.x_acceleration = self.factory.aircraft.sensors.accelerometer.x
        sensor_data_response.accelerometer.y_acceleration = self.factory.aircraft.sensors.accelerometer.y
        sensor_data_response.accelerometer.z_acceleration = self.factory.aircraft.sensors.accelerometer.z

    def fill_gyroscope_data(self, sensor_data_response):
        sensor_data_response.type = fdm_pb2.GYROSCOPE_REQUEST

        sensor_data_response.gyroscope.roll_rate = self.factory.aircraft.gyroscope.roll_rate
        sensor_data_response.gyroscope.pitch_rate = self.factory.aircraft.gyroscope.pitch_rate
        sensor_data_response.gyroscope.yaw_rate = self.factory.aircraft.gyroscope.yaw_rate

    def fill_thermometer_data(self, sensor_data_response):
        sensor_data_response.type = fdm_pb2.THERMOMETER_REQUEST

        sensor_data_response.thermometer.temperature = self.factory.aircraft.thermometer.temperature

    def fill_pressure_sensor_data(self, sensor_data_response):
        sensor_data_response.type = fdm_pb2.PRESSURE_SENSOR_REQUEST

        sensor_data_response.pressure_sensor.pressure = self.factory.aircraft.pressure_sensor.pressure

    def fill_pitot_tube_data(self, sensor_data_response):
        sensor_data_response.type = fdm_pb2.PITOT_TUBE_REQUEST

        sensor_data_response.pitot_tube.pressure = self.factory.aircraft.pitot_tube.pressure

    def fill_engine_data(self, sensor_data_response):
        sensor_data_response.type = fdm_pb2.ENGINE_REQUEST

        sensor_data_response.engine.thrust = self.factory.aircraft.engine.thrust
        sensor_data_response.engine.throttle = self.factory.aircraft.engine.throttle

    def fill_controls_data(self, sensor_data_response):
        sensor_data_response.type = fdm_pb2.CONTROLS_REQUEST

        sensor_data_response.controls.aileron = self.factory.aircraft.controls.aileron
        sensor_data_response.controls.elevator = self.factory.aircraft.controls.elevator
        sensor_data_response.controls.rudder = self.factory.aircraft.controls.rudder
        sensor_data_response.controls.throttle = self.factory.aircraft.engine.throttle

    def fill_ins_data(self, sensor_data_response):
        sensor_data_response.type = fdm_pb2.INS_REQUEST

        sensor_data_response.ins.roll = self.factory.aircraft.inertial_navigation_system.roll
        sensor_data_response.ins.pitch = self.factory.aircraft.inertial_navigation_system.pitch

    def fill_error_response(self, sensor_data_response):
        sensor_data_response.type = fdm_pb2.INVALID_REQUEST

    def send_response_string(self, response_string):
        self.sendString(response_string)

        self.transport.loseConnection()

    def handle_sensor_data_request(self, sensor_data_request):
        """Fills the required data on the response object and sends the
        response back to the requesting client"""
        sensor_data_response = fdm_pb2.SensorDataResponse()

        if sensor_data_request.type == fdm_pb2.GPS_REQUEST:
            self.fill_gps_data(sensor_data_response)
        elif sensor_data_request.type == fdm_pb2.ACCELEROMETER_REQUEST:
            self.fill_accelerometer_data(sensor_data_response)
        elif sensor_data_request.type == fdm_pb2.GYROSCOPE_REQUEST:
            self.fill_accelerometer_data(sensor_data_response)
        elif sensor_data_request.type == fdm_pb2.THERMOMETER_REQUEST:
            self.fill_thermometer_data(sensor_data_response)
        elif sensor_data_request.type == fdm_pb2.PRESSURE_SENSOR_REQUEST:
            self.fill_pressure_sensor_data(sensor_data_response)
        elif sensor_data_request.type == fdm_pb2.PITOT_TUBE_REQUEST:
            self.fill_pitot_tube_data(sensor_data_response)
        elif sensor_data_request.type == fdm_pb2.ENGINE_REQUEST:
            self.fill_engine_data(sensor_data_response)
        elif sensor_data_request.type == fdm_pb2.CONTROLS_REQUEST:
            self.fill_controls_data(sensor_data_response)
        elif sensor_data_request.type == fdm_pb2.INS_REQUEST:
            self.fill_ins_data(sensor_data_response)
        else:
            self.fill_error_response(sensor_data_response)

        self.send_response_string(sensor_data_response.SerializeToString())

    def stringReceived(self, string):
        sensor_data_request = fdm_pb2.SensorDataRequest()
        sensor_data_request.ParseFromString(string)

        self.handle_sensor_data_request(sensor_data_request)

class SensorDataFactory(Factory):
    def __init__(self, aircraft):
        self.protocol = SensorDataProtocol
        self.aircraft = aircraft

class SensorDataResponceListener(object):
    def received_responce(self, sensor_data_responce):
        pass

class SensorDataClientProtocol(Int32StringReceiver):
    def connectionMade(self):
        sensor_data_request = fdm_pb2.SensorDataRequest()
        sensor_data_request.type = self.factory.request_type

        self.sendString(sensor_data_request.SerializeToString())

    def stringReceived(self, string):
        sensor_data_response = fdm_pb2.SensorDataResponse()
        sensor_data_response.ParseFromString(string)

        self.factory.received_responce(sensor_data_response)

class SensorDataClientProtocolFactory(Factory):
    def __init__(self, request_type, sensor_data_responce_listener):
        self.protocol = SensorDataClientProtocol
        self.request_type = request_type
        self.sensor_data_responce_listener = sensor_data_responce_listener

    def received_responce(self, sensor_data_responce):
        self.sensor_data_responce_listener.received_responce(sensor_data_responce)
