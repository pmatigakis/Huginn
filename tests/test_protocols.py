from unittest import TestCase
import math

from mock import MagicMock
from twisted.test.proto_helpers import StringTransport

from huginn.protocols import ControlsProtocol, TelemetryFactory, TelemetryProtocol,\
                             FDMDataProtocol, TelemetryClientFactory,\
                             FDMDataClient, ControlsClient, SensorDataProtocol,\
                             SensorDataFactory
from huginn.aircraft import Aircraft
from huginn import fdm_pb2

from mockObjects import MockFDMExec, MockTelemetryDataListener,\
                        MockFDMDataDatagram, MockFDMDataListener

class TestControlsProtocol(TestCase):                
    def test_datagram_received(self):
        fdmexec = MockFDMExec()
        
        aircraft = Aircraft(fdmexec)
        aircraft.run()
        
        controls_protocol = ControlsProtocol(aircraft)
             
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

class TestTelemetryFactory(TestCase):
    def test_get_telemetry_data(self):
        fdmexec = MockFDMExec()

        aircraft = Aircraft(fdmexec)
        aircraft.run()

        factory = TelemetryFactory(aircraft)
        protocol = TelemetryProtocol(factory)

        telemetry_data = factory.get_telemetry_data()

        self.assertEqual(len(telemetry_data), len(protocol.telemetry_items))

        for item in protocol.telemetry_items:
            self.assertTrue(telemetry_data.has_key(item))

        self.assertAlmostEqual(telemetry_data["time"], fdmexec.GetSimTime(), 3)
        self.assertAlmostEqual(telemetry_data["dt"], fdmexec.GetDeltaT(), 3)
        self.assertAlmostEqual(telemetry_data["latitude"], aircraft.gps.latitude, 3)
        self.assertAlmostEqual(telemetry_data["longitude"], aircraft.gps.longitude, 3)
        self.assertAlmostEqual(telemetry_data["altitude"], aircraft.gps.altitude, 3)
        self.assertAlmostEqual(telemetry_data["airspeed"], aircraft.gps.airspeed, 3)
        self.assertAlmostEqual(telemetry_data["heading"], aircraft.gps.heading, 3)
        self.assertAlmostEqual(telemetry_data["x_acceleration"], aircraft.accelerometer.x_acceleration, 3)
        self.assertAlmostEqual(telemetry_data["y_acceleration"], aircraft.accelerometer.y_acceleration, 3)
        self.assertAlmostEqual(telemetry_data["z_acceleration"], aircraft.accelerometer.z_acceleration, 3)
        self.assertAlmostEqual(telemetry_data["roll_rate"], aircraft.gyroscope.roll_rate, 3)
        self.assertAlmostEqual(telemetry_data["pitch_rate"], aircraft.gyroscope.pitch_rate, 3)
        self.assertAlmostEqual(telemetry_data["yaw_rate"], aircraft.gyroscope.yaw_rate, 3)
        self.assertAlmostEqual(telemetry_data["temperature"], aircraft.thermometer.temperature, 3)
        self.assertAlmostEqual(telemetry_data["static_pressure"], aircraft.pressure_sensor.pressure, 3)
        self.assertAlmostEqual(telemetry_data["dynamic_pressure"], aircraft.pitot_tube.pressure, 3)
        self.assertAlmostEqual(telemetry_data["roll"], aircraft.inertial_navigation_system.roll, 3)
        self.assertAlmostEqual(telemetry_data["pitch"], aircraft.inertial_navigation_system.pitch, 3)
        self.assertAlmostEqual(telemetry_data["thrust"], aircraft.engine.thrust, 3)
        self.assertAlmostEqual(telemetry_data["aileron"], aircraft.controls.aileron, 3)
        self.assertAlmostEqual(telemetry_data["elevator"], aircraft.controls.elevator, 3)
        self.assertAlmostEqual(telemetry_data["rudder"], aircraft.controls.rudder, 3)
        self.assertAlmostEqual(telemetry_data["throttle"], aircraft.engine.throttle, 3)

class TestFDMDataProtocol(TestCase):
    def test_get_fdm_data(self):
        fdmexec = MockFDMExec()

        aircraft = Aircraft(fdmexec)
        aircraft.run()

        fdm_data_protocol = FDMDataProtocol(aircraft, "127.0.0.1", 12345)

        fdm_data = fdm_data_protocol.get_fdm_data()

        self.assertAlmostEqual(fdm_data.time, fdmexec.GetSimTime(), 3)
        self.assertAlmostEqual(fdm_data.gps.latitude, aircraft.gps.latitude, 3)
        self.assertAlmostEqual(fdm_data.gps.longitude, aircraft.gps.longitude, 3)
        self.assertAlmostEqual(fdm_data.gps.altitude, aircraft.gps.altitude, 3)
        self.assertAlmostEqual(fdm_data.gps.airspeed, aircraft.gps.airspeed, 3)
        self.assertAlmostEqual(fdm_data.gps.heading, aircraft.gps.heading, 3)
        self.assertAlmostEqual(fdm_data.accelerometer.x_acceleration, aircraft.accelerometer.x_acceleration, 3)
        self.assertAlmostEqual(fdm_data.accelerometer.y_acceleration, aircraft.accelerometer.y_acceleration, 3)
        self.assertAlmostEqual(fdm_data.accelerometer.z_acceleration, aircraft.accelerometer.z_acceleration, 3)
        self.assertAlmostEqual(fdm_data.gyroscope.roll_rate, aircraft.gyroscope.roll_rate, 3)
        self.assertAlmostEqual(fdm_data.gyroscope.pitch_rate, aircraft.gyroscope.pitch_rate, 3)
        self.assertAlmostEqual(fdm_data.gyroscope.yaw_rate, aircraft.gyroscope.yaw_rate, 3)
        self.assertAlmostEqual(fdm_data.thermometer.temperature, aircraft.thermometer.temperature, 3)
        self.assertAlmostEqual(fdm_data.pressure_sensor.pressure, aircraft.pressure_sensor.pressure, 3)
        self.assertAlmostEqual(fdm_data.pitot_tube.pressure, aircraft.pitot_tube.pressure, 3)
        self.assertAlmostEqual(fdm_data.ins.roll, aircraft.inertial_navigation_system.roll, 3)
        self.assertAlmostEqual(fdm_data.ins.pitch, aircraft.inertial_navigation_system.pitch, 3)
        self.assertAlmostEqual(fdm_data.engine.thrust, aircraft.engine.thrust, 3)
        self.assertAlmostEqual(fdm_data.engine.throttle, aircraft.engine.throttle, 3)
        self.assertAlmostEqual(fdm_data.controls.aileron, aircraft.controls.aileron, 3)
        self.assertAlmostEqual(fdm_data.controls.elevator, aircraft.controls.elevator, 3)
        self.assertAlmostEqual(fdm_data.controls.rudder, aircraft.controls.rudder, 3)
        self.assertAlmostEqual(fdm_data.controls.throttle, aircraft.controls.throttle, 3)

class TestTelemetryClientfactory(TestCase):
    def test_notify_listeners_on_telemetry_data_reception(self):
        factory = TelemetryClientFactory()
        protocol = factory.buildProtocol(("127.0.0.1", 0))
        transport = StringTransport()

        mock_telemetry_data_listener_1 = MockTelemetryDataListener()
        factory.add_telemetry_listener(mock_telemetry_data_listener_1)

        mock_telemetry_data_listener_2 = MockTelemetryDataListener()
        factory.add_telemetry_listener(mock_telemetry_data_listener_2)

        protocol.makeConnection(transport)

        mock_telemetry_data_listener_1.received_telemetry_header = MagicMock()
        mock_telemetry_data_listener_1.received_telemetry_data = MagicMock()

        mock_telemetry_data_listener_2.received_telemetry_header = MagicMock()
        mock_telemetry_data_listener_2.received_telemetry_data = MagicMock()

        protocol.lineReceived("time,dt,latitude,longitude,altitude,airspeed,heading")
        protocol.lineReceived("10.0,0.001,35.00000,24.00000,1000.0,50.0,132.12")

        mock_telemetry_data_listener_1.received_telemetry_data.assert_called_with(["10.0", "0.001", "35.00000", "24.00000", "1000.0", "50.0", "132.12"])
        mock_telemetry_data_listener_2.received_telemetry_data.assert_called_with(["10.0", "0.001", "35.00000", "24.00000", "1000.0", "50.0", "132.12"])

        protocol.lineReceived("10.001,0.001,35.00001,24.00001,1000.1,50.1,132.13")

        mock_telemetry_data_listener_1.received_telemetry_data.assert_called_with(["10.001", "0.001", "35.00001", "24.00001", "1000.1", "50.1", "132.13"])
        mock_telemetry_data_listener_2.received_telemetry_data.assert_called_with(["10.001", "0.001", "35.00001", "24.00001", "1000.1", "50.1", "132.13"])

        mock_telemetry_data_listener_1.received_telemetry_header.assert_called_once_with(["time", "dt", "latitude", "longitude", "altitude", "airspeed", "heading"])
        mock_telemetry_data_listener_2.received_telemetry_header.assert_called_once_with(["time", "dt", "latitude", "longitude", "altitude", "airspeed", "heading"])

def isclose(number_1, number_2, tolerance):
    d = math.fabs(number_1 - number_2)
    
    if d > tolerance:
        return False
    
    return True

class FDMDataMatcher(object):
    def __eq__(self, fdm_data):
        mock_fdm_data_datagram = MockFDMDataDatagram()

        if not isclose(fdm_data.time, mock_fdm_data_datagram.simulation_time, 0.001): return False

        if not isclose(fdm_data.gps.latitude, mock_fdm_data_datagram.latitude, 0.001): return False

        if not isclose(fdm_data.gps.longitude, mock_fdm_data_datagram.longitude, 0.001): return False

        if not isclose(fdm_data.gps.altitude, mock_fdm_data_datagram.altitude, 0.001): return False

        if not isclose(fdm_data.gps.airspeed, mock_fdm_data_datagram.airspeed, 0.001): return False

        if not isclose(fdm_data.gps.heading, mock_fdm_data_datagram.heading, 0.001): return False

        if not isclose(fdm_data.accelerometer.x_acceleration, mock_fdm_data_datagram.x_acceleration, 0.001): return False

        if not isclose(fdm_data.accelerometer.y_acceleration, mock_fdm_data_datagram.y_acceleration, 0.001): return False

        if not isclose(fdm_data.accelerometer.z_acceleration, mock_fdm_data_datagram.z_acceleration, 0.001): return False

        if not isclose(fdm_data.gyroscope.roll_rate, mock_fdm_data_datagram.roll_rate, 0.001): return False

        if not isclose(fdm_data.gyroscope.pitch_rate, mock_fdm_data_datagram.pitch_rate, 0.001): return False

        if not isclose(fdm_data.gyroscope.yaw_rate, mock_fdm_data_datagram.yaw_rate, 0.001): return False

        if not isclose(fdm_data.thermometer.temperature, mock_fdm_data_datagram.temperature, 0.001): return False

        if not isclose(fdm_data.pressure_sensor.pressure, mock_fdm_data_datagram.static_pressure, 0.001): return False

        if not isclose(fdm_data.pitot_tube.pressure, mock_fdm_data_datagram.total_pressure, 0.001): return False

        if not isclose(fdm_data.ins.roll, mock_fdm_data_datagram.roll, 0.001): return False

        if not isclose(fdm_data.ins.pitch, mock_fdm_data_datagram.pitch, 0.001): return False

        if not isclose(fdm_data.engine.thrust, mock_fdm_data_datagram.thrust, 0.001): return False

        if not isclose(fdm_data.controls.aileron, mock_fdm_data_datagram.aileron, 0.001): return False

        if not isclose(fdm_data.controls.elevator, mock_fdm_data_datagram.elevator, 0.001): return False

        if not isclose(fdm_data.controls.rudder, mock_fdm_data_datagram.rudder, 0.001): return False

        if not isclose(fdm_data.controls.throttle, mock_fdm_data_datagram.throttle, 0.001): return False

        return True

class TestFDMDataClient(TestCase):
    def test_received_fdm_data_datagram(self):
        fdm_data_client = FDMDataClient()

        mock_fdm_data_listener = MockFDMDataListener()
        mock_fdm_data_listener.fdm_data_received = MagicMock()

        fdm_data_client.add_fdm_data_listener(mock_fdm_data_listener)

        mock_fdm_data_datagram = MockFDMDataDatagram().create_datagram()

        fdm_data_client.datagramReceived(mock_fdm_data_datagram, ("127.0.0.1", 12345))

        mock_fdm_data_listener.fdm_data_received.assert_called_once_with(FDMDataMatcher())

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
        fdmexec = MockFDMExec()

        aircraft = Aircraft(fdmexec)
        
        aircraft.run()

        factory = SensorDataFactory(aircraft)
        
        protocol = factory.buildProtocol(("127.0.0.1", 12345))

        sensor_data_response = fdm_pb2.SensorDataResponse()

        protocol.fill_gps_data(sensor_data_response)

        self.assertAlmostEqual(sensor_data_response.gps.latitude, aircraft.gps.latitude)
        self.assertAlmostEqual(sensor_data_response.gps.longitude, aircraft.gps.longitude)
        self.assertAlmostEqual(sensor_data_response.gps.altitude, aircraft.gps.altitude)
        self.assertAlmostEqual(sensor_data_response.gps.airspeed, aircraft.gps.airspeed)
        self.assertAlmostEqual(sensor_data_response.gps.heading, aircraft.gps.heading)

        self.assertEqual(sensor_data_response.type, fdm_pb2.GPS_REQUEST)

    def test_fill_accelerometer_data(self):
        fdmexec = MockFDMExec()

        aircraft = Aircraft(fdmexec)
        
        aircraft.run()

        factory = SensorDataFactory(aircraft)
        
        protocol = factory.buildProtocol(("127.0.0.1", 12345))

        sensor_data_response = fdm_pb2.SensorDataResponse()

        protocol.fill_accelerometer_data(sensor_data_response)

        self.assertAlmostEqual(sensor_data_response.accelerometer.x_acceleration, aircraft.accelerometer.x_acceleration)
        self.assertAlmostEqual(sensor_data_response.accelerometer.y_acceleration, aircraft.accelerometer.y_acceleration)
        self.assertAlmostEqual(sensor_data_response.accelerometer.z_acceleration, aircraft.accelerometer.z_acceleration)

        self.assertEqual(sensor_data_response.type, fdm_pb2.ACCELEROMETER_REQUEST)

    def test_fill_gyroscope_data(self):
        fdmexec = MockFDMExec()

        aircraft = Aircraft(fdmexec)
        
        aircraft.run()

        factory = SensorDataFactory(aircraft)
        
        protocol = factory.buildProtocol(("127.0.0.1", 12345))

        sensor_data_response = fdm_pb2.SensorDataResponse()

        protocol.fill_gyroscope_data(sensor_data_response)

        self.assertAlmostEqual(sensor_data_response.gyroscope.roll_rate, aircraft.gyroscope.roll_rate)
        self.assertAlmostEqual(sensor_data_response.gyroscope.pitch_rate, aircraft.gyroscope.pitch_rate)
        self.assertAlmostEqual(sensor_data_response.gyroscope.yaw_rate, aircraft.gyroscope.yaw_rate)

        self.assertEqual(sensor_data_response.type, fdm_pb2.GYROSCOPE_REQUEST)

    def test_fill_thermometer_data(self):
        fdmexec = MockFDMExec()

        aircraft = Aircraft(fdmexec)
        
        aircraft.run()

        factory = SensorDataFactory(aircraft)
        
        protocol = factory.buildProtocol(("127.0.0.1", 12345))

        sensor_data_response = fdm_pb2.SensorDataResponse()

        protocol.fill_thermometer_data(sensor_data_response)

        self.assertAlmostEqual(sensor_data_response.thermometer.temperature, aircraft.thermometer.temperature)

        self.assertEqual(sensor_data_response.type, fdm_pb2.THERMOMETER_REQUEST)

    def test_fill_pressure_sensor_data(self):
        fdmexec = MockFDMExec()

        aircraft = Aircraft(fdmexec)
        
        aircraft.run()

        factory = SensorDataFactory(aircraft)
        
        protocol = factory.buildProtocol(("127.0.0.1", 12345))

        sensor_data_response = fdm_pb2.SensorDataResponse()

        protocol.fill_pressure_sensor_data(sensor_data_response)

        self.assertAlmostEqual(sensor_data_response.pressure_sensor.pressure, aircraft.pressure_sensor.pressure)

        self.assertEqual(sensor_data_response.type, fdm_pb2.PRESSURE_SENSOR_REQUEST)

    def test_fill_pitot_tube_data(self):
        fdmexec = MockFDMExec()

        aircraft = Aircraft(fdmexec)
        
        aircraft.run()

        factory = SensorDataFactory(aircraft)
        
        protocol = factory.buildProtocol(("127.0.0.1", 12345))

        sensor_data_response = fdm_pb2.SensorDataResponse()

        protocol.fill_pitot_tube_data(sensor_data_response)

        self.assertAlmostEqual(sensor_data_response.pitot_tube.pressure, aircraft.pitot_tube.pressure)

        self.assertEqual(sensor_data_response.type, fdm_pb2.PITOT_TUBE_REQUEST)

    def test_fill_engine_data(self):
        fdmexec = MockFDMExec()

        aircraft = Aircraft(fdmexec)
        
        aircraft.run()

        factory = SensorDataFactory(aircraft)
        
        protocol = factory.buildProtocol(("127.0.0.1", 12345))

        sensor_data_response = fdm_pb2.SensorDataResponse()

        protocol.fill_engine_data(sensor_data_response)

        self.assertAlmostEqual(sensor_data_response.engine.thrust, aircraft.engine.thrust)
        self.assertAlmostEqual(sensor_data_response.engine.throttle, aircraft.engine.throttle)

        self.assertEqual(sensor_data_response.type, fdm_pb2.ENGINE_REQUEST)

    def test_fill_controls_data(self):
        fdmexec = MockFDMExec()

        aircraft = Aircraft(fdmexec)
        
        aircraft.run()

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
        fdmexec = MockFDMExec()

        aircraft = Aircraft(fdmexec)
        
        aircraft.run()

        factory = SensorDataFactory(aircraft)
        
        protocol = factory.buildProtocol(("127.0.0.1", 12345))

        sensor_data_response = fdm_pb2.SensorDataResponse()

        protocol.fill_ins_data(sensor_data_response)

        self.assertAlmostEqual(sensor_data_response.ins.roll, aircraft.inertial_navigation_system.roll)
        self.assertAlmostEqual(sensor_data_response.ins.pitch, aircraft.inertial_navigation_system.pitch)

        self.assertEqual(sensor_data_response.type, fdm_pb2.INS_REQUEST)

    def test_handle_sensor_data_request(self):
        fdmexec = MockFDMExec()

        aircraft = Aircraft(fdmexec)
        
        aircraft.run()

        factory = SensorDataFactory(aircraft)
        
        protocol = factory.buildProtocol(("127.0.0.1", 12345))
        protocol.send_response_string = MagicMock()

        sensor_data_request = fdm_pb2.SensorDataRequest()
        sensor_data_request.type = fdm_pb2.GPS_REQUEST

        protocol.handle_sensor_data_request(sensor_data_request)

        expected_sensor_data_response = fdm_pb2.SensorDataResponse()
        expected_sensor_data_response.type = fdm_pb2.GPS_REQUEST
        expected_sensor_data_response.gps.latitude = aircraft.gps.latitude
        expected_sensor_data_response.gps.longitude = aircraft.gps.longitude
        expected_sensor_data_response.gps.altitude = aircraft.gps.altitude
        expected_sensor_data_response.gps.airspeed = aircraft.gps.airspeed
        expected_sensor_data_response.gps.heading = aircraft.gps.heading
        
        protocol.send_response_string.assert_called_once_with(expected_sensor_data_response.SerializeToString())
