"""
The huginn.protocols module contains classes that are used by twisted in order
to transmit and receive simulation data.
"""


import logging
from abc import ABCMeta, abstractmethod

from twisted.internet.protocol import DatagramProtocol, Factory
from twisted.protocols.basic import Int32StringReceiver
from google.protobuf.message import DecodeError

from huginn.protobuf import fdm_pb2


logger = logging.getLogger(__name__)


class ControlsProtocol(DatagramProtocol):
    """The ControlsProtocol is used to receive and update tha aircraft's
    controls"""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

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
            logger.exception("Failed to parse control data")
            print("Failed to parse control data")
            return

        self.update_aircraft_controls(controls.aileron,
                                      controls.elevator,
                                      controls.rudder,
                                      controls.throttle)


class SimulatorDataProtocol(DatagramProtocol):
    """The FDMDataProtocol class is used to transmit the flight dynamics model
    data to the client"""
    def __init__(self, simulator, remote_host, port):
        self.simulator = simulator
        self.fdmexec = simulator.fdmexec
        self.aircraft = simulator.aircraft
        self.remote_host = remote_host
        self.port = port

    def _fill_gps_data(self, simulator_data):
        """Fill the gps data in the SimulatorData object

        Arguments:
        simulator_data: the protocol buffer SimulatorData object
        """
        simulator_data.gps.latitude = self.aircraft.instruments.gps.latitude
        simulator_data.gps.longitude = self.aircraft.instruments.gps.longitude
        simulator_data.gps.altitude = self.aircraft.instruments.gps.altitude
        simulator_data.gps.airspeed = self.aircraft.instruments.gps.airspeed
        simulator_data.gps.heading = self.aircraft.instruments.gps.heading

    def _fill_accelerometer_data(self, simulator_data):
        """Fill the accelerometer data in the SimulatorData object

        Arguments:
        simulator_data: the protocol buffer SimulatorData object
        """
        sensors = self.aircraft.sensors

        simulator_data.accelerometer.x = sensors.accelerometer.x
        simulator_data.accelerometer.y = sensors.accelerometer.y
        simulator_data.accelerometer.z = sensors.accelerometer.z

    def _fill_gyroscope_data(self, simulator_data):
        """Fill the gyroscope data in the SimulatorData object

        Arguments:
        simulator_data: the protocol buffer SimulatorData object
        """
        sensors = self.aircraft.sensors

        simulator_data.gyroscope.roll_rate = sensors.gyroscope.roll_rate
        simulator_data.gyroscope.pitch_rate = sensors.gyroscope.pitch_rate
        simulator_data.gyroscope.yaw_rate = sensors.gyroscope.yaw_rate

    def _fill_thermometer_data(self, simulator_data):
        """Fill the thermometer data in the SimulatorData object

        Arguments:
        simulator_data: the protocol buffer SimulatorData object
        """
        thermometer = self.aircraft.sensors.thermometer

        simulator_data.thermometer.temperature = thermometer.temperature

    def _fill_pressure_sensor_data(self, simulator_data):
        """Fill the pressure sensor data in the SimulatorData object

        Arguments:
        simulator_data: the protocol buffer SimulatorData object
        """
        pressure_sensor = self.aircraft.sensors.pressure_sensor
        pitot_tube = self.aircraft.sensors.pitot_tube

        simulator_data.pressure_sensor.pressure = pressure_sensor.pressure
        simulator_data.pitot_tube.pressure = pitot_tube.pressure

    def _fill_engine_data(self, simulator_data):
        """Fill the engine data in the SimulatorData object

        Arguments:
        simulator_data: the protocol buffer SimulatorData object
        """
        simulator_data.engine.thrust = self.aircraft.engine.thrust
        simulator_data.engine.throttle = self.aircraft.engine.throttle

    def _fill_aircraft_controls_data(self, simulator_data):
        """Fill the aircraft controls data in the SimulatorData object

        Arguments:
        simulator_data: the protocol buffer SimulatorData object
        """
        simulator_data.controls.aileron = self.aircraft.controls.aileron
        simulator_data.controls.elevator = self.aircraft.controls.elevator
        simulator_data.controls.rudder = self.aircraft.controls.rudder
        simulator_data.controls.throttle = self.aircraft.controls.throttle

    def _fill_ins_data(self, simulator_data):
        """Fill the inertial navigation system data in the SimulatorData
        object

        Arguments:
        simulator_data: the protocol buffer SimulatorData object
        """
        ins = self.aircraft.sensors.inertial_navigation_system

        simulator_data.ins.roll = ins.roll
        simulator_data.ins.pitch = ins.pitch
        simulator_data.ins.latitude = ins.latitude
        simulator_data.ins.longitude = ins.longitude
        simulator_data.ins.altitude = ins.altitude
        simulator_data.ins.airspeed = ins.airspeed
        simulator_data.ins.heading = ins.heading

    def _fill_accelerations(self, simulator_data):
        """Fill the fdm accelerations data in the SimulatorData object

        Arguments:
        simulator_data: the protocol buffer SimulatorData object
        """
        accelerations = self.simulator.fdm.accelerations

        simulator_data.accelerations.x = accelerations.x
        simulator_data.accelerations.y = accelerations.y
        simulator_data.accelerations.z = accelerations.z
        simulator_data.accelerations.p_dot = accelerations.p_dot
        simulator_data.accelerations.q_dot = accelerations.q_dot
        simulator_data.accelerations.r_dot = accelerations.r_dot
        simulator_data.accelerations.u_dot = accelerations.u_dot
        simulator_data.accelerations.v_dot = accelerations.v_dot
        simulator_data.accelerations.w_dot = accelerations.w_dot
        simulator_data.accelerations.gravity = accelerations.gravity

    def _fill_velocities(self, simulator_data):
        """Fill the fdm velocities data in the SimulatorData object

        Arguments:
        simulator_data: the protocol buffer SimulatorData object
        """
        velocities = self.simulator.fdm.velocities

        simulator_data.velocities.p = velocities.p
        simulator_data.velocities.q = velocities.q
        simulator_data.velocities.r = velocities.r
        simulator_data.velocities.u = velocities.u
        simulator_data.velocities.v = velocities.v
        simulator_data.velocities.w = velocities.w
        simulator_data.velocities.true_airspeed = velocities.true_airspeed

        calibrated_airspeed = velocities.calibrated_airspeed
        simulator_data.velocities.calibrated_airspeed = calibrated_airspeed

        equivalent_airspeed = velocities.equivalent_airspeed
        simulator_data.velocities.equivalent_airspeed = equivalent_airspeed

        simulator_data.velocities.climb_rate = velocities.climb_rate
        simulator_data.velocities.ground_speed = velocities.ground_speed

    def _fill_position(self, simulator_data):
        """Fill the fdm position data in the SimulatorData object

        Arguments:
        simulator_data: the protocol buffer SimulatorData object
        """
        position = self.simulator.fdm.position

        simulator_data.position.latitude = position.latitude
        simulator_data.position.longitude = position.longitude
        simulator_data.position.altitude = position.altitude
        simulator_data.position.heading = position.heading

    def _fill_orientation(self, simulator_data):
        """Fill the fdm orientation data in the SimulatorData object

        Arguments:
        simulator_data: the protocol buffer SimulatorData object
        """
        orientation = self.simulator.fdm.orientation

        simulator_data.orientation.phi = orientation.phi
        simulator_data.orientation.theta = orientation.theta
        simulator_data.orientation.psi = orientation.psi

    def _fill_atmosphere(self, simulator_data):
        """Fill the fdm atmospheric data in the SimulatorData object

        Arguments:
        simulator_data: the protocol buffer SimulatorData object
        """
        atmosphere = self.simulator.fdm.atmosphere

        simulator_data.atmosphere.pressure = atmosphere.pressure

        sea_level_pressure = atmosphere.sea_level_pressure
        simulator_data.atmosphere.sea_level_pressure = sea_level_pressure

        simulator_data.atmosphere.temperature = atmosphere.temperature

        sea_level_temperature = atmosphere.sea_level_temperature
        simulator_data.atmosphere.sea_level_temperature = sea_level_temperature

        simulator_data.atmosphere.density = atmosphere.density

        sea_level_density = atmosphere.sea_level_density
        simulator_data.atmosphere.sea_level_density = sea_level_density 

    def get_simulator_data(self):
        """Return the simulator data"""
        simulator_data = fdm_pb2.SimulatorData()

        simulator_data.time = self.fdmexec.GetSimTime()

        self._fill_gps_data(simulator_data)
        self._fill_accelerometer_data(simulator_data)
        self._fill_gyroscope_data(simulator_data)
        self._fill_thermometer_data(simulator_data)
        self._fill_pressure_sensor_data(simulator_data)
        self._fill_engine_data(simulator_data)
        self._fill_aircraft_controls_data(simulator_data)
        self._fill_ins_data(simulator_data)
        self._fill_accelerations(simulator_data)
        self._fill_velocities(simulator_data)
        self._fill_position(simulator_data)
        self._fill_orientation(simulator_data)
        self._fill_atmosphere(simulator_data)

        return simulator_data

    def send_simulator_data(self):
        """Transmit the simulator data"""
        simulator_data = self.get_simulator_data()

        datagram = simulator_data.SerializeToString()

        self.transport.write(datagram, (self.remote_host, self.port))


class SimulatorDataListener(object):
    """The methods of the FDMDataListener class must be implemented by any
    object that wants to handle the fdm data received from Huginn"""
    __metaclass = ABCMeta

    @abstractmethod
    def simulator_data_received(self, simulator_data):
        """This function is called when simulator data have been received so
        that the implementing class can handler them

        Arguments:
        simulator_data: a protocol buffer object that contains the fdm data
        """
        pass


class SimulatorDataClient(DatagramProtocol):
    """The SimulatorDataClient is used to receive simulator data from
    Huginn"""

    def __init__(self):
        self.listeners = []

    def add_simulator_data_listener(self, listener):
        """Add an simulator data listener"""
        self.listeners.append(listener)

    def remove_simulator_data_listener(self, listener):
        """Remove an simulator data listener"""
        self.listeners.remove(listener)

    def _notify_simulator_data_listeners(self, simulator_data):
        """Update the simulator data listeners

        Arguments:
        simulator_data: a protocol buffer object that contains the simulator
            data
        """
        for simulator_data_listener in self.listeners:
            simulator_data_listener.simulator_data_received(simulator_data)

    def datagramReceived(self, datagram, addr):
        simulator_data = fdm_pb2.SimulatorData()

        simulator_data.ParseFromString(datagram)

        self._notify_simulator_data_listeners(simulator_data)


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

        instruments = self.factory.aircraft.instruments
        sensor_data_response.gps.latitude = instruments.gps.latitude
        sensor_data_response.gps.longitude = instruments.gps.longitude
        sensor_data_response.gps.altitude = instruments.gps.altitude
        sensor_data_response.gps.airspeed = instruments.gps.airspeed
        sensor_data_response.gps.heading = instruments.gps.heading

    def fill_accelerometer_data(self, sensor_data_response):
        sensor_data_response.type = fdm_pb2.ACCELEROMETER_REQUEST

        accelerometer = self.factory.aircraft.sensors.accelerometer

        sensor_data_response.accelerometer.x = accelerometer.x
        sensor_data_response.accelerometer.y = accelerometer.y
        sensor_data_response.accelerometer.z = accelerometer.z

    def fill_gyroscope_data(self, sensor_data_response):
        sensor_data_response.type = fdm_pb2.GYROSCOPE_REQUEST

        gyroscope = self.factory.aircraft.sensors.gyroscope

        sensor_data_response.gyroscope.roll_rate = gyroscope.roll_rate
        sensor_data_response.gyroscope.pitch_rate = gyroscope.pitch_rate
        sensor_data_response.gyroscope.yaw_rate = gyroscope.yaw_rate

    def fill_thermometer_data(self, sensor_data_response):
        sensor_data_response.type = fdm_pb2.THERMOMETER_REQUEST

        thermometer = self.factory.aircraft.sensors.thermometer

        sensor_data_response.thermometer.temperature = thermometer.temperature

    def fill_pressure_sensor_data(self, sensor_data_response):
        sensor_data_response.type = fdm_pb2.PRESSURE_SENSOR_REQUEST

        pressure = self.factory.aircraft.sensors.pressure_sensor.pressure

        sensor_data_response.pressure_sensor.pressure = pressure

    def fill_pitot_tube_data(self, sensor_data_response):
        sensor_data_response.type = fdm_pb2.PITOT_TUBE_REQUEST

        pitot_tube = self.factory.aircraft.sensors.pitot_tube

        sensor_data_response.pitot_tube.pressure = pitot_tube.pressure

    def fill_engine_data(self, sensor_data_response):
        sensor_data_response.type = fdm_pb2.ENGINE_REQUEST

        engine = self.factory.aircraft.engine

        sensor_data_response.engine.thrust = engine.thrust
        sensor_data_response.engine.throttle = engine.throttle

    def fill_controls_data(self, sensor_data_response):
        sensor_data_response.type = fdm_pb2.CONTROLS_REQUEST

        controls = self.factory.aircraft.controls
        engine = self.factory.aircraft.engine

        sensor_data_response.controls.aileron = controls.aileron
        sensor_data_response.controls.elevator = controls.elevator
        sensor_data_response.controls.rudder = controls.rudder
        sensor_data_response.controls.throttle = engine.throttle

    def fill_ins_data(self, sensor_data_response):
        sensor_data_response.type = fdm_pb2.INS_REQUEST

        ins = self.factory.aircraft.sensors.inertial_navigation_system

        sensor_data_response.ins.roll = ins.roll
        sensor_data_response.ins.pitch = ins.pitch
        sensor_data_response.ins.latitude = ins.latitude
        sensor_data_response.ins.longitude = ins.longitude
        sensor_data_response.ins.altitude = ins.altitude
        sensor_data_response.ins.airspeed = ins.airspeed
        sensor_data_response.ins.heading = ins.heading

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
        self.sensor_data_responce_listener.received_responce(
            sensor_data_responce
        )
