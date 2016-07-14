from unittest import TestCase

from mock import MagicMock

from huginn.protocols import ControlsProtocol, SimulatorDataProtocol,\
                             SimulatorDataClient, ControlsClient,\
                             SensorDataFactory
from huginn.aircraft import Aircraft
from huginn.protobuf import fdm_pb2
from huginn.fdm import FDMBuilder, FDM
from huginn import configuration
from huginn.simulator import Simulator

from test_common import isclose

from mockObjects import MockSimulatorDataDatagram, MockSimulatorDataListener

class TestControlsProtocol(TestCase):                
    def test_datagram_received(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()
        
        aircraft = Aircraft(fdmexec)
        
        controls_protocol = ControlsProtocol(fdmexec)
             
        aileron = 0.1
        elevator = 0.2
        rudder = 0.3
        throttle = 0.4
    
        controls = fdm_pb2.Controls()
        controls.aileron = aileron
        controls.elevator = elevator
        controls.rudder = rudder
        controls.throttle = throttle
        
        controls_datagram = controls.SerializeToString()
             
        host = "127.0.0.1"
        port = 12345
             
        controls_protocol.datagramReceived(controls_datagram, (host, port))
        
        self.assertAlmostEqual(aircraft.controls.aileron, aileron, 3)
        self.assertAlmostEqual(aircraft.controls.elevator, elevator, 3)
        self.assertAlmostEqual(aircraft.controls.rudder, rudder, 3)
        self.assertAlmostEqual(aircraft.controls.throttle, throttle, 3)

class TestSimulatorDataProtocol(TestCase):
    def test_get_simulator_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        simulator = Simulator(fdmexec)

        aircraft = simulator.aircraft
        fdm = simulator.fdm

        simulator_data_protocol = SimulatorDataProtocol(simulator, "127.0.0.1", 12345)

        simulator_data = simulator_data_protocol.get_simulator_data()

        self.assertAlmostEqual(simulator_data.time, fdmexec.GetSimTime(), 3)
        self.assertAlmostEqual(simulator_data.gps.latitude, aircraft.instruments.gps.latitude, 3)
        self.assertAlmostEqual(simulator_data.gps.longitude, aircraft.instruments.gps.longitude, 3)
        self.assertAlmostEqual(simulator_data.gps.altitude, aircraft.instruments.gps.altitude, 3)
        self.assertAlmostEqual(simulator_data.gps.airspeed, aircraft.instruments.gps.airspeed, 3)
        self.assertAlmostEqual(simulator_data.gps.heading, aircraft.instruments.gps.heading, 3)
        self.assertAlmostEqual(simulator_data.accelerometer.x, aircraft.sensors.accelerometer.x, 3)
        self.assertAlmostEqual(simulator_data.accelerometer.y, aircraft.sensors.accelerometer.y, 3)
        self.assertAlmostEqual(simulator_data.accelerometer.z, aircraft.sensors.accelerometer.z, 3)
        self.assertAlmostEqual(simulator_data.gyroscope.roll_rate, aircraft.sensors.gyroscope.roll_rate, 3)
        self.assertAlmostEqual(simulator_data.gyroscope.pitch_rate, aircraft.sensors.gyroscope.pitch_rate, 3)
        self.assertAlmostEqual(simulator_data.gyroscope.yaw_rate, aircraft.sensors.gyroscope.yaw_rate, 3)
        self.assertAlmostEqual(simulator_data.thermometer.temperature, aircraft.sensors.thermometer.temperature, 3)
        self.assertAlmostEqual(simulator_data.pressure_sensor.pressure, aircraft.sensors.pressure_sensor.pressure, 3)
        self.assertAlmostEqual(simulator_data.pitot_tube.pressure, aircraft.sensors.pitot_tube.pressure, 3)
        self.assertAlmostEqual(simulator_data.ins.roll, aircraft.sensors.inertial_navigation_system.roll, 3)
        self.assertAlmostEqual(simulator_data.ins.pitch, aircraft.sensors.inertial_navigation_system.pitch, 3)
        self.assertAlmostEqual(simulator_data.ins.latitude, aircraft.sensors.inertial_navigation_system.latitude, 3)
        self.assertAlmostEqual(simulator_data.ins.longitude, aircraft.sensors.inertial_navigation_system.longitude, 3)
        self.assertAlmostEqual(simulator_data.ins.altitude, aircraft.sensors.inertial_navigation_system.altitude, 3)
        self.assertAlmostEqual(simulator_data.ins.airspeed, aircraft.sensors.inertial_navigation_system.airspeed, 3)
        self.assertAlmostEqual(simulator_data.ins.heading, aircraft.sensors.inertial_navigation_system.heading, 3)
        self.assertAlmostEqual(simulator_data.engine.thrust, aircraft.engine.thrust, 3)
        self.assertAlmostEqual(simulator_data.engine.throttle, aircraft.engine.throttle, 3)
        self.assertAlmostEqual(simulator_data.controls.aileron, aircraft.controls.aileron, 3)
        self.assertAlmostEqual(simulator_data.controls.elevator, aircraft.controls.elevator, 3)
        self.assertAlmostEqual(simulator_data.controls.rudder, aircraft.controls.rudder, 3)
        self.assertAlmostEqual(simulator_data.controls.throttle, aircraft.controls.throttle, 3)
        self.assertAlmostEqual(simulator_data.accelerations.x, fdm.accelerations.x, 3)
        self.assertAlmostEqual(simulator_data.accelerations.y, fdm.accelerations.y, 3)
        self.assertAlmostEqual(simulator_data.accelerations.z, fdm.accelerations.z, 3)
        self.assertAlmostEqual(simulator_data.accelerations.p_dot, fdm.accelerations.p_dot, 3)
        self.assertAlmostEqual(simulator_data.accelerations.q_dot, fdm.accelerations.q_dot, 3)
        self.assertAlmostEqual(simulator_data.accelerations.r_dot, fdm.accelerations.r_dot, 3)
        self.assertAlmostEqual(simulator_data.accelerations.u_dot, fdm.accelerations.u_dot, 3)
        self.assertAlmostEqual(simulator_data.accelerations.v_dot, fdm.accelerations.v_dot, 3)
        self.assertAlmostEqual(simulator_data.accelerations.w_dot, fdm.accelerations.w_dot, 3)
        self.assertAlmostEqual(simulator_data.accelerations.gravity, fdm.accelerations.gravity, 3)
        
        self.assertAlmostEqual(simulator_data.velocities.p, fdm.velocities.p, 3)
        self.assertAlmostEqual(simulator_data.velocities.q, fdm.velocities.q, 3)
        self.assertAlmostEqual(simulator_data.velocities.r, fdm.velocities.r, 3)
        self.assertAlmostEqual(simulator_data.velocities.true_airspeed, fdm.velocities.true_airspeed, 3)
        self.assertAlmostEqual(simulator_data.velocities.climb_rate, fdm.velocities.climb_rate, 3)
        self.assertAlmostEqual(simulator_data.velocities.u, fdm.velocities.u, 3)
        self.assertAlmostEqual(simulator_data.velocities.v, fdm.velocities.v, 3)
        self.assertAlmostEqual(simulator_data.velocities.w, fdm.velocities.w, 3)
        self.assertAlmostEqual(simulator_data.velocities.calibrated_airspeed, fdm.velocities.calibrated_airspeed, 3)
        self.assertAlmostEqual(simulator_data.velocities.equivalent_airspeed, fdm.velocities.equivalent_airspeed, 3)
        self.assertAlmostEqual(simulator_data.velocities.ground_speed, fdm.velocities.ground_speed, 3)

        self.assertAlmostEqual(simulator_data.position.latitude, fdm.position.latitude, 3)
        self.assertAlmostEqual(simulator_data.position.longitude, fdm.position.longitude, 3)
        self.assertAlmostEqual(simulator_data.position.altitude, fdm.position.altitude, 3)
        self.assertAlmostEqual(simulator_data.position.heading, fdm.position.heading, 3)

        self.assertAlmostEqual(simulator_data.orientation.phi, fdm.orientation.phi, 3)
        self.assertAlmostEqual(simulator_data.orientation.theta, fdm.orientation.theta, 3)
        self.assertAlmostEqual(simulator_data.orientation.psi, fdm.orientation.psi, 3)

        self.assertAlmostEqual(simulator_data.atmosphere.pressure, fdm.atmosphere.pressure, 3)
        self.assertAlmostEqual(simulator_data.atmosphere.sea_level_pressure, fdm.atmosphere.sea_level_pressure, 3)
        self.assertAlmostEqual(simulator_data.atmosphere.temperature, fdm.atmosphere.temperature, 3)
        self.assertAlmostEqual(simulator_data.atmosphere.sea_level_temperature, fdm.atmosphere.sea_level_temperature, 3)
        self.assertAlmostEqual(simulator_data.atmosphere.density, fdm.atmosphere.density, 3)
        self.assertAlmostEqual(simulator_data.atmosphere.sea_level_density, fdm.atmosphere.sea_level_density, 3)

class SimulatorDataMatcher(object):
    def __eq__(self, fdm_data):
        mock_simulator_data_datagram = MockSimulatorDataDatagram()

        if not isclose(fdm_data.time, mock_simulator_data_datagram.simulation_time, 0.001): return False
        if not isclose(fdm_data.gps.latitude, mock_simulator_data_datagram.latitude, 0.001): return False
        if not isclose(fdm_data.gps.longitude, mock_simulator_data_datagram.longitude, 0.001): return False
        if not isclose(fdm_data.gps.altitude, mock_simulator_data_datagram.altitude, 0.001): return False
        if not isclose(fdm_data.gps.airspeed, mock_simulator_data_datagram.airspeed, 0.001): return False
        if not isclose(fdm_data.gps.heading, mock_simulator_data_datagram.heading, 0.001): return False
        if not isclose(fdm_data.accelerometer.x, mock_simulator_data_datagram.x_acceleration, 0.001): return False
        if not isclose(fdm_data.accelerometer.y, mock_simulator_data_datagram.y_acceleration, 0.001): return False
        if not isclose(fdm_data.accelerometer.z, mock_simulator_data_datagram.z_acceleration, 0.001): return False
        if not isclose(fdm_data.gyroscope.roll_rate, mock_simulator_data_datagram.roll_rate, 0.001): return False
        if not isclose(fdm_data.gyroscope.pitch_rate, mock_simulator_data_datagram.pitch_rate, 0.001): return False
        if not isclose(fdm_data.gyroscope.yaw_rate, mock_simulator_data_datagram.yaw_rate, 0.001): return False
        if not isclose(fdm_data.thermometer.temperature, mock_simulator_data_datagram.temperature, 0.001): return False
        if not isclose(fdm_data.pressure_sensor.pressure, mock_simulator_data_datagram.static_pressure, 0.001): return False
        if not isclose(fdm_data.pitot_tube.pressure, mock_simulator_data_datagram.total_pressure, 0.001): return False
        if not isclose(fdm_data.ins.roll, mock_simulator_data_datagram.roll, 0.001): return False
        if not isclose(fdm_data.ins.pitch, mock_simulator_data_datagram.pitch, 0.001): return False
        if not isclose(fdm_data.ins.latitude, mock_simulator_data_datagram.latitude, 0.001): return False
        if not isclose(fdm_data.ins.longitude, mock_simulator_data_datagram.longitude, 0.001): return False
        if not isclose(fdm_data.ins.altitude, mock_simulator_data_datagram.altitude, 0.001): return False
        if not isclose(fdm_data.ins.airspeed, mock_simulator_data_datagram.airspeed, 0.001): return False
        if not isclose(fdm_data.ins.heading, mock_simulator_data_datagram.heading, 0.001): return False
        if not isclose(fdm_data.engine.thrust, mock_simulator_data_datagram.thrust, 0.001): return False
        if not isclose(fdm_data.controls.aileron, mock_simulator_data_datagram.aileron, 0.001): return False
        if not isclose(fdm_data.controls.elevator, mock_simulator_data_datagram.elevator, 0.001): return False
        if not isclose(fdm_data.controls.rudder, mock_simulator_data_datagram.rudder, 0.001): return False
        if not isclose(fdm_data.controls.throttle, mock_simulator_data_datagram.throttle, 0.001): return False
        if not isclose(fdm_data.accelerations.x, mock_simulator_data_datagram.fdm_x_acceleration, 0.001): return False
        if not isclose(fdm_data.accelerations.y, mock_simulator_data_datagram.fdm_y_acceleration, 0.001): return False
        if not isclose(fdm_data.accelerations.z, mock_simulator_data_datagram.fdm_z_acceleration, 0.001): return False
        if not isclose(fdm_data.accelerations.p_dot, mock_simulator_data_datagram.p_dot, 0.001): return False
        if not isclose(fdm_data.accelerations.q_dot, mock_simulator_data_datagram.q_dot, 0.001): return False
        if not isclose(fdm_data.accelerations.r_dot, mock_simulator_data_datagram.r_dot, 0.001): return False
        if not isclose(fdm_data.accelerations.u_dot, mock_simulator_data_datagram.u_dot, 0.001): return False
        if not isclose(fdm_data.accelerations.v_dot, mock_simulator_data_datagram.v_dot, 0.001): return False
        if not isclose(fdm_data.accelerations.w_dot, mock_simulator_data_datagram.w_dot, 0.001): return False
        if not isclose(fdm_data.accelerations.gravity, mock_simulator_data_datagram.gravity, 0.001): return False
        
        if not isclose(fdm_data.velocities.p, mock_simulator_data_datagram.p, 0.001): return False
        if not isclose(fdm_data.velocities.q, mock_simulator_data_datagram.q, 0.001): return False
        if not isclose(fdm_data.velocities.r, mock_simulator_data_datagram.r, 0.001): return False
        if not isclose(fdm_data.velocities.true_airspeed, mock_simulator_data_datagram.true_airspeed, 0.001): return False
        if not isclose(fdm_data.velocities.climb_rate, mock_simulator_data_datagram.climb_rate, 0.001): return False
        if not isclose(fdm_data.velocities.u, mock_simulator_data_datagram.u, 0.001): return False
        if not isclose(fdm_data.velocities.v, mock_simulator_data_datagram.v, 0.001): return False
        if not isclose(fdm_data.velocities.w, mock_simulator_data_datagram.w, 0.001): return False
        if not isclose(fdm_data.velocities.calibrated_airspeed, mock_simulator_data_datagram.calibrated_airspeed, 0.001): return False
        if not isclose(fdm_data.velocities.equivalent_airspeed, mock_simulator_data_datagram.equivalent_airspeed, 0.001): return False
        if not isclose(fdm_data.velocities.ground_speed, mock_simulator_data_datagram.ground_speed, 0.001): return False

        if not isclose(fdm_data.position.latitude, mock_simulator_data_datagram.fdm_latitude, 0.001): return False
        if not isclose(fdm_data.position.longitude, mock_simulator_data_datagram.fdm_longitude, 0.001): return False
        if not isclose(fdm_data.position.altitude, mock_simulator_data_datagram.fdm_altitude, 0.001): return False
        if not isclose(fdm_data.position.heading, mock_simulator_data_datagram.fdm_heading, 0.001): return False

        if not isclose(fdm_data.orientation.phi, mock_simulator_data_datagram.phi, 0.001): return False
        if not isclose(fdm_data.orientation.theta, mock_simulator_data_datagram.theta, 0.001): return False
        if not isclose(fdm_data.orientation.psi, mock_simulator_data_datagram.psi, 0.001): return False

        if not isclose(fdm_data.atmosphere.pressure, mock_simulator_data_datagram.fdm_pressure, 0.001): return False
        if not isclose(fdm_data.atmosphere.sea_level_pressure, mock_simulator_data_datagram.fdm_sea_level_pressure, 0.001): return False
        if not isclose(fdm_data.atmosphere.temperature, mock_simulator_data_datagram.fdm_temperature, 0.001): return False
        if not isclose(fdm_data.atmosphere.sea_level_temperature, mock_simulator_data_datagram.fdm_sea_level_temperature, 0.001): return False
        if not isclose(fdm_data.atmosphere.density, mock_simulator_data_datagram.fdm_density, 0.001): return False
        if not isclose(fdm_data.atmosphere.sea_level_density, mock_simulator_data_datagram.fdm_sea_level_density, 0.001): return False

        return True

class TestSimulatorDataClient(TestCase):
    def test_received_simulator_data_datagram(self):
        simulator_data_client = SimulatorDataClient()

        mock_simulator_data_listener = MockSimulatorDataListener()
        mock_simulator_data_listener.simulator_data_received = MagicMock()

        simulator_data_client.add_simulator_data_listener(mock_simulator_data_listener)

        mock_simulator_data_datagram = MockSimulatorDataDatagram().create_datagram()

        simulator_data_client.datagramReceived(mock_simulator_data_datagram, ("127.0.0.1", 12345))

        mock_simulator_data_listener.simulator_data_received.assert_called_once_with(SimulatorDataMatcher())

class TestControlsClient(TestCase):
    def test_transmit_controls(self):
        protocol = ControlsClient("127.0.0.1", 12345)
        protocol.send_datagram = MagicMock(0)

        protocol.transmit_controls(0.1, 0.2, 0.3, 0.4)

        controls_data = fdm_pb2.Controls()
        controls_data.aileron = 0.1
        controls_data.elevator = 0.2
        controls_data.rudder = 0.3
        controls_data.throttle = 0.4

        expected_datagram = controls_data.SerializeToString()

        protocol.send_datagram.assert_called_once_with(expected_datagram)

class TestSensorDataProtocol(TestCase):
    def test_fill_gps_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        factory = SensorDataFactory(aircraft)
        
        protocol = factory.buildProtocol(("127.0.0.1", 12345))

        sensor_data_response = fdm_pb2.SensorDataResponse()

        protocol.fill_gps_data(sensor_data_response)

        self.assertAlmostEqual(sensor_data_response.gps.latitude, aircraft.instruments.gps.latitude)
        self.assertAlmostEqual(sensor_data_response.gps.longitude, aircraft.instruments.gps.longitude)
        self.assertAlmostEqual(sensor_data_response.gps.altitude, aircraft.instruments.gps.altitude)
        self.assertAlmostEqual(sensor_data_response.gps.airspeed, aircraft.instruments.gps.airspeed)
        self.assertAlmostEqual(sensor_data_response.gps.heading, aircraft.instruments.gps.heading)

        self.assertEqual(sensor_data_response.type, fdm_pb2.GPS_REQUEST)

    def test_fill_accelerometer_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        factory = SensorDataFactory(aircraft)
        
        protocol = factory.buildProtocol(("127.0.0.1", 12345))

        sensor_data_response = fdm_pb2.SensorDataResponse()

        protocol.fill_accelerometer_data(sensor_data_response)

        self.assertAlmostEqual(sensor_data_response.accelerometer.x, aircraft.sensors.accelerometer.x)
        self.assertAlmostEqual(sensor_data_response.accelerometer.y, aircraft.sensors.accelerometer.y)
        self.assertAlmostEqual(sensor_data_response.accelerometer.z, aircraft.sensors.accelerometer.z)

        self.assertEqual(sensor_data_response.type, fdm_pb2.ACCELEROMETER_REQUEST)

    def test_fill_gyroscope_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        factory = SensorDataFactory(aircraft)
        
        protocol = factory.buildProtocol(("127.0.0.1", 12345))

        sensor_data_response = fdm_pb2.SensorDataResponse()

        protocol.fill_gyroscope_data(sensor_data_response)

        self.assertAlmostEqual(sensor_data_response.gyroscope.roll_rate, aircraft.sensors.gyroscope.roll_rate)
        self.assertAlmostEqual(sensor_data_response.gyroscope.pitch_rate, aircraft.sensors.gyroscope.pitch_rate)
        self.assertAlmostEqual(sensor_data_response.gyroscope.yaw_rate, aircraft.sensors.gyroscope.yaw_rate)

        self.assertEqual(sensor_data_response.type, fdm_pb2.GYROSCOPE_REQUEST)

    def test_fill_thermometer_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        factory = SensorDataFactory(aircraft)
        
        protocol = factory.buildProtocol(("127.0.0.1", 12345))

        sensor_data_response = fdm_pb2.SensorDataResponse()

        protocol.fill_thermometer_data(sensor_data_response)

        self.assertAlmostEqual(sensor_data_response.thermometer.temperature, aircraft.sensors.thermometer.temperature)

        self.assertEqual(sensor_data_response.type, fdm_pb2.THERMOMETER_REQUEST)

    def test_fill_pressure_sensor_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        factory = SensorDataFactory(aircraft)
        
        protocol = factory.buildProtocol(("127.0.0.1", 12345))

        sensor_data_response = fdm_pb2.SensorDataResponse()

        protocol.fill_pressure_sensor_data(sensor_data_response)

        self.assertAlmostEqual(sensor_data_response.pressure_sensor.pressure, aircraft.sensors.pressure_sensor.pressure)

        self.assertEqual(sensor_data_response.type, fdm_pb2.PRESSURE_SENSOR_REQUEST)

    def test_fill_pitot_tube_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        factory = SensorDataFactory(aircraft)
        
        protocol = factory.buildProtocol(("127.0.0.1", 12345))

        sensor_data_response = fdm_pb2.SensorDataResponse()

        protocol.fill_pitot_tube_data(sensor_data_response)

        self.assertAlmostEqual(sensor_data_response.pitot_tube.pressure, aircraft.sensors.pitot_tube.pressure)

        self.assertEqual(sensor_data_response.type, fdm_pb2.PITOT_TUBE_REQUEST)

    def test_fill_engine_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        factory = SensorDataFactory(aircraft)
        
        protocol = factory.buildProtocol(("127.0.0.1", 12345))

        sensor_data_response = fdm_pb2.SensorDataResponse()

        protocol.fill_engine_data(sensor_data_response)

        self.assertAlmostEqual(sensor_data_response.engine.thrust, aircraft.engine.thrust)
        self.assertAlmostEqual(sensor_data_response.engine.throttle, aircraft.engine.throttle)

        self.assertEqual(sensor_data_response.type, fdm_pb2.ENGINE_REQUEST)

    def test_fill_controls_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        factory = SensorDataFactory(aircraft)
        
        protocol = factory.buildProtocol(("127.0.0.1", 12345))

        sensor_data_response = fdm_pb2.SensorDataResponse()

        protocol.fill_controls_data(sensor_data_response)

        self.assertAlmostEqual(sensor_data_response.controls.aileron, aircraft.controls.aileron)
        self.assertAlmostEqual(sensor_data_response.controls.elevator, aircraft.controls.elevator)
        self.assertAlmostEqual(sensor_data_response.controls.rudder, aircraft.controls.rudder)
        self.assertAlmostEqual(sensor_data_response.controls.throttle, aircraft.controls.throttle)

        self.assertEqual(sensor_data_response.type, fdm_pb2.CONTROLS_REQUEST)

    def test_fill_ins_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        factory = SensorDataFactory(aircraft)
        
        protocol = factory.buildProtocol(("127.0.0.1", 12345))

        sensor_data_response = fdm_pb2.SensorDataResponse()

        protocol.fill_ins_data(sensor_data_response)

        self.assertAlmostEqual(sensor_data_response.ins.roll, aircraft.sensors.inertial_navigation_system.roll)
        self.assertAlmostEqual(sensor_data_response.ins.pitch, aircraft.sensors.inertial_navigation_system.pitch)

        self.assertEqual(sensor_data_response.type, fdm_pb2.INS_REQUEST)

    def test_handle_sensor_data_request(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()
 
        aircraft = Aircraft(fdmexec)

        factory = SensorDataFactory(aircraft)
        
        protocol = factory.buildProtocol(("127.0.0.1", 12345))
        protocol.send_response_string = MagicMock()

        sensor_data_request = fdm_pb2.SensorDataRequest()
        sensor_data_request.type = fdm_pb2.GPS_REQUEST

        protocol.handle_sensor_data_request(sensor_data_request)

        expected_sensor_data_response = fdm_pb2.SensorDataResponse()
        expected_sensor_data_response.type = fdm_pb2.GPS_REQUEST
        expected_sensor_data_response.gps.latitude = aircraft.instruments.gps.latitude
        expected_sensor_data_response.gps.longitude = aircraft.instruments.gps.longitude
        expected_sensor_data_response.gps.altitude = aircraft.instruments.gps.altitude
        expected_sensor_data_response.gps.airspeed = aircraft.instruments.gps.airspeed
        expected_sensor_data_response.gps.heading = aircraft.instruments.gps.heading
        
        protocol.send_response_string.assert_called_once_with(expected_sensor_data_response.SerializeToString())
