import struct
from unittest import TestCase
import math

from mock import MagicMock
from hamcrest import close_to
from hamcrest.library.integration import match_equality
from twisted.test.proto_helpers import StringTransport, FakeDatagramTransport

from huginn.protocols import SensorDataProtocol, SensorDataRequest,  SensorDataResponse,  ERROR_CODE,\
    SENSOR_DATA_RESPONCE_OK, ControlsProtocol, GPS_DATA_REQUEST,\
    ACCELEROMETER_DATA_REQUEST, GYROSCOPE_DATA_REQUEST,\
    MAGNETOMETER_DATA_REQUEST, THERMOMETER_DATA_REQUEST, PITOT_TUBE_DATA_REQUEST,\
    STATIC_PRESSURE_DATA_REQUEST, INS_DATA_REQUEST,\
    TelemetryFactory, TelemetryProtocol, FDMDataProtocol, TelemetryClientFactory,\
    decode_fdm_data_datagram, FDMDataClient, ControlsClient
from huginn.aircraft import C172P

from mockObjects import MockFDMModel, MockFDMExec, MockTelemetryDataListener,\
                        MockFDMDataDatagram, MockFDMDataListener

class TestSensorDataProtocol(TestCase):
    def test_decode_request(self):
        fdm_model = MockFDMModel()

        aircraft = C172P(fdm_model)

        sensor_data_protocol = SensorDataProtocol(aircraft)

        request_datagram = struct.pack("!c", chr(GPS_DATA_REQUEST))
        host = "127.0.0.1"
        port = 12345

        request = sensor_data_protocol.decode_request(request_datagram, host, port)

        self.assertIsInstance(request, SensorDataRequest)
        self.assertEqual(request.host, host)
        self.assertEqual(request.port, port)
        self.assertEqual(request.command, GPS_DATA_REQUEST)
          
    def test_return_error_code_on_invalid_request_datagram(self):
        fdm_model = MockFDMModel()

        aircraft = C172P(fdm_model)

        sensor_data_protocol = SensorDataProtocol(aircraft)

        sensor_data_protocol.transmit_error_code = MagicMock()

        request_datagram = struct.pack("!cc", chr(GPS_DATA_REQUEST), chr(0x00))
        host = "127.0.0.1"
        port = 12345
               
        sensor_data_protocol.datagramReceived(request_datagram, (host, port))

        sensor_data_protocol.transmit_error_code.assert_called_once_with(ERROR_CODE, host, port)

    def test_return_error_code_on_invalid_request_command(self):
        fdm_model = MockFDMModel()

        aircraft = C172P(fdm_model)

        sensor_data_protocol = SensorDataProtocol(aircraft)
            
        sensor_data_protocol.transmit_error_code = MagicMock()

        request_datagram = struct.pack("!cc", chr(0x50), chr(0x00))
        host = "127.0.0.1"
        port = 12345
    
        sensor_data_protocol.datagramReceived(request_datagram, (host, port))

        sensor_data_protocol.transmit_error_code.assert_called_once_with(ERROR_CODE, host, port)

    def test_create_gps_data_response(self):
        fdm_model = MockFDMModel()

        aircraft = C172P(fdm_model)

        request = SensorDataRequest("127.0.0.1", 12345, GPS_DATA_REQUEST)

        sensor_data_protocol = SensorDataProtocol(aircraft)

        response = sensor_data_protocol.create_gps_data_response(request)

        self.assertEqual(len(response.sensor_values), 5)
        self.assertEqual(response.sensor_data_request, request)

        self.assertAlmostEqual(response.sensor_values[0], aircraft.gps.latitude, 3)
        self.assertAlmostEqual(response.sensor_values[1], aircraft.gps.longitude, 3)
        self.assertAlmostEqual(response.sensor_values[2], aircraft.gps.altitude, 3)
        self.assertAlmostEqual(response.sensor_values[3], aircraft.gps.airspeed, 3)
        self.assertAlmostEqual(response.sensor_values[4], aircraft.gps.heading, 3)

    def test_create_accelerometer_data_response(self):
        fdm_model = MockFDMModel()

        aircraft = C172P(fdm_model)

        request = SensorDataRequest("127.0.0.1", 12345, ACCELEROMETER_DATA_REQUEST)

        sensor_data_protocol = SensorDataProtocol(aircraft)

        response = sensor_data_protocol.create_accelerometer_data_response(request)

        self.assertEqual(len(response.sensor_values), 3)
        self.assertEqual(response.sensor_data_request, request)

        self.assertAlmostEqual(response.sensor_values[0], aircraft.accelerometer.x_acceleration, 3)
        self.assertAlmostEqual(response.sensor_values[1], aircraft.accelerometer.y_acceleration, 3)
        self.assertAlmostEqual(response.sensor_values[2], aircraft.accelerometer.z_acceleration, 3)

    def test_create_gyroscope_data_response(self):
        fdm_model = MockFDMModel()

        aircraft = C172P(fdm_model)

        request = SensorDataRequest("127.0.0.1", 12345, GYROSCOPE_DATA_REQUEST)

        sensor_data_protocol = SensorDataProtocol(aircraft)

        response = sensor_data_protocol.create_gyroscope_data_response(request)

        self.assertEqual(len(response.sensor_values), 3)
        self.assertEqual(response.sensor_data_request, request)

        self.assertAlmostEqual(response.sensor_values[0], aircraft.gyroscope.roll_rate, 3)
        self.assertAlmostEqual(response.sensor_values[1], aircraft.gyroscope.pitch_rate, 3)
        self.assertAlmostEqual(response.sensor_values[2], aircraft.gyroscope.yaw_rate, 3)

    def test_create_magnetometer_data_response(self):
        fdm_model = MockFDMModel()

        aircraft = C172P(fdm_model)

        request = SensorDataRequest("127.0.0.1", 12345, MAGNETOMETER_DATA_REQUEST)

        sensor_data_protocol = SensorDataProtocol(aircraft)

        response = sensor_data_protocol.create_magnetometer_data_response(request)

        self.assertEqual(len(response.sensor_values), 3)
        self.assertEqual(response.sensor_data_request, request)

        self.assertAlmostEqual(response.sensor_values[0], 0.0, 3)
        self.assertAlmostEqual(response.sensor_values[1], 0.0, 3)
        self.assertAlmostEqual(response.sensor_values[2], 0.0, 3)

    def test_create_thermometer_data_response(self):
        fdm_model = MockFDMModel()

        aircraft = C172P(fdm_model)

        request = SensorDataRequest("127.0.0.1", 12345, THERMOMETER_DATA_REQUEST)

        sensor_data_protocol = SensorDataProtocol(aircraft)

        response = sensor_data_protocol.create_thermometer_data_response(request)

        self.assertEqual(len(response.sensor_values), 1)
        self.assertEqual(response.sensor_data_request, request)

        self.assertAlmostEqual(response.sensor_values[0], aircraft.thermometer.temperature, 3)

    def test_create_pitot_tube_data_response(self):
        fdm_model = MockFDMModel()

        aircraft = C172P(fdm_model)

        request = SensorDataRequest("127.0.0.1", 12345, PITOT_TUBE_DATA_REQUEST)

        sensor_data_protocol = SensorDataProtocol(aircraft)

        response = sensor_data_protocol.create_pitot_tube_data_response(request)

        self.assertEqual(len(response.sensor_values), 1)
        self.assertEqual(response.sensor_data_request, request)

        self.assertAlmostEqual(response.sensor_values[0], aircraft.pitot_tube.pressure, 3)

    def test_create_static_pressure_data_response(self):
        fdm_model = MockFDMModel()

        aircraft = C172P(fdm_model)

        request = SensorDataRequest("127.0.0.1", 12345, STATIC_PRESSURE_DATA_REQUEST)

        sensor_data_protocol = SensorDataProtocol(aircraft)

        response = sensor_data_protocol.create_static_pressure_data_response(request)

        self.assertEqual(len(response.sensor_values), 1)
        self.assertEqual(response.sensor_data_request, request)

        self.assertAlmostEqual(response.sensor_values[0], aircraft.pressure_sensor.pressure, 3)

    def test_create_ins_data_response(self):
        fdm_model = MockFDMModel()
        
        aircraft = C172P(fdm_model)
            
        request = SensorDataRequest("127.0.0.1", 12345, INS_DATA_REQUEST)
            
        sensor_data_protocol = SensorDataProtocol(aircraft)
            
        response = sensor_data_protocol.create_ins_data_response(request)
    
        self.assertEqual(len(response.sensor_values), 7)
        self.assertEqual(response.sensor_data_request, request)
            
        self.assertAlmostEqual(response.sensor_values[0], aircraft.inertial_navigation_system.roll, 3)
        self.assertAlmostEqual(response.sensor_values[1], aircraft.inertial_navigation_system.pitch, 3)
        self.assertAlmostEqual(response.sensor_values[2], aircraft.inertial_navigation_system.heading, 3)
        self.assertAlmostEqual(response.sensor_values[3], aircraft.inertial_navigation_system.latitude, 3)
        self.assertAlmostEqual(response.sensor_values[4], aircraft.inertial_navigation_system.longitude, 3)
        self.assertAlmostEqual(response.sensor_values[5], aircraft.inertial_navigation_system.airspeed, 3)
        self.assertAlmostEqual(response.sensor_values[6], aircraft.inertial_navigation_system.altitude, 3)

class TestSensorDataResponse(TestCase):
    def test_encode_response(self):
        sensor_data_request = SensorDataRequest("127.0.0.1", 12345, GPS_DATA_REQUEST)

        sensor_values = [1.0, 2.0, 3.0, 4.0, 5.0]

        sensor_data_response = SensorDataResponse(sensor_data_request,
                                                  sensor_values)

        encoded_response = sensor_data_response.encode_response()

        decoded_reponse = struct.unpack("!ccfffff", encoded_response)

        self.assertEqual(ord(decoded_reponse[0]), SENSOR_DATA_RESPONCE_OK)
        self.assertEqual(ord(decoded_reponse[1]), GPS_DATA_REQUEST)
        self.assertAlmostEqual(decoded_reponse[2], 1.0)
        self.assertAlmostEqual(decoded_reponse[3], 2.0)
        self.assertAlmostEqual(decoded_reponse[4], 3.0)
        self.assertAlmostEqual(decoded_reponse[5], 4.0)
        self.assertAlmostEqual(decoded_reponse[6], 5.0)

class TestControlsProtocol(TestCase):                
    def test_datagram_received(self):
        fdm_model = MockFDMModel()
        
        aircraft = C172P(fdm_model)
        
        controls_protocol = ControlsProtocol(aircraft)
        controls_protocol.update_aircraft_controls = MagicMock()
             
        aileron = 0.1
        elevator = 0.2
        rudder = 0.3
        throttle = 0.4
             
        controls_datagram = struct.pack("!ffff", aileron, elevator, rudder, throttle)
             
        host = "127.0.0.1"
        port = 12345
             
        controls_protocol.datagramReceived(controls_datagram, (host, port))
        
        controls_protocol.update_aircraft_controls.assert_called_once_with(match_equality(close_to(aileron, 0.001)),
                                                                           match_equality(close_to(elevator, 0.001)),
                                                                           match_equality(close_to(rudder, 0.001)),
                                                                           match_equality(close_to(throttle, 0.001)))

class TestTelemetryFactory(TestCase):
    def test_get_telemetry_data(self):
        fdmexec = MockFDMExec()

        aircraft = C172P(fdmexec)

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

        aircraft = C172P(fdmexec)

        fdm_data_protocol = FDMDataProtocol(aircraft, "127.0.0.1", 12345)

        fdm_data = fdm_data_protocol.get_fdm_data()

        self.assertEqual(len(fdm_data), 22)

        self.assertAlmostEqual(fdm_data[0], fdmexec.GetSimTime(), 3)
        self.assertAlmostEqual(fdm_data[1], aircraft.gps.latitude, 3)
        self.assertAlmostEqual(fdm_data[2], aircraft.gps.longitude, 3)
        self.assertAlmostEqual(fdm_data[3], aircraft.gps.altitude, 3)
        self.assertAlmostEqual(fdm_data[4], aircraft.gps.airspeed, 3)
        self.assertAlmostEqual(fdm_data[5], aircraft.gps.heading, 3)
        self.assertAlmostEqual(fdm_data[6], aircraft.accelerometer.x_acceleration, 3)
        self.assertAlmostEqual(fdm_data[7], aircraft.accelerometer.y_acceleration, 3)
        self.assertAlmostEqual(fdm_data[8], aircraft.accelerometer.z_acceleration, 3)
        self.assertAlmostEqual(fdm_data[9], aircraft.gyroscope.roll_rate, 3)
        self.assertAlmostEqual(fdm_data[10], aircraft.gyroscope.pitch_rate, 3)
        self.assertAlmostEqual(fdm_data[11], aircraft.gyroscope.yaw_rate, 3)
        self.assertAlmostEqual(fdm_data[12], aircraft.thermometer.temperature, 3)
        self.assertAlmostEqual(fdm_data[13], aircraft.pressure_sensor.pressure, 3)
        self.assertAlmostEqual(fdm_data[14], aircraft.pitot_tube.pressure, 3)
        self.assertAlmostEqual(fdm_data[15], aircraft.inertial_navigation_system.roll, 3)
        self.assertAlmostEqual(fdm_data[16], aircraft.inertial_navigation_system.pitch, 3)
        self.assertAlmostEqual(fdm_data[17], aircraft.engine.thrust, 3)
        self.assertAlmostEqual(fdm_data[18], aircraft.controls.aileron, 3)
        self.assertAlmostEqual(fdm_data[19], aircraft.controls.elevator, 3)
        self.assertAlmostEqual(fdm_data[20], aircraft.controls.rudder, 3)
        self.assertAlmostEqual(fdm_data[21], aircraft.engine.throttle, 3)

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

class TestDecodeFDMDataDatagram(TestCase):
    def test_raise_exception_on_invalid_datagram(self):
        mock_fdm_datagram = MockFDMDataDatagram()

        fdm_data_datagram = mock_fdm_datagram.create_invalid_datagram()

        self.assertRaises(struct.error, decode_fdm_data_datagram, fdm_data_datagram)

    def test_decode_fdm_data_datagram(self):
        mock_fdm_datagram = MockFDMDataDatagram()

        fdm_data_datagram = mock_fdm_datagram.create_datagram()

        fdm_data = decode_fdm_data_datagram(fdm_data_datagram)

        self.assertEquals(len(fdm_data), 22)
        
        self.assertTrue(fdm_data.has_key("time"))
        self.assertAlmostEqual(fdm_data["time"], mock_fdm_datagram.simulation_time, 3)

        self.assertTrue(fdm_data.has_key("latitude"))
        self.assertAlmostEqual(fdm_data["latitude"], mock_fdm_datagram.latitude, 3)

        self.assertTrue(fdm_data.has_key("longitude"))
        self.assertAlmostEqual(fdm_data["longitude"], mock_fdm_datagram.longitude, 3)

        self.assertTrue(fdm_data.has_key("altitude"))
        self.assertAlmostEqual(fdm_data["altitude"], mock_fdm_datagram.altitude, 3)

        self.assertTrue(fdm_data.has_key("airspeed"))
        self.assertAlmostEqual(fdm_data["airspeed"], mock_fdm_datagram.airspeed, 3)

        self.assertTrue(fdm_data.has_key("heading"))
        self.assertAlmostEqual(fdm_data["heading"], mock_fdm_datagram.heading, 3)

        self.assertTrue(fdm_data.has_key("x_acceleration"))
        self.assertAlmostEqual(fdm_data["x_acceleration"], mock_fdm_datagram.x_acceleration, 3)

        self.assertTrue(fdm_data.has_key("y_acceleration"))
        self.assertAlmostEqual(fdm_data["y_acceleration"], mock_fdm_datagram.y_acceleration, 3)

        self.assertTrue(fdm_data.has_key("z_acceleration"))
        self.assertAlmostEqual(fdm_data["z_acceleration"], mock_fdm_datagram.z_acceleration, 3)

        self.assertTrue(fdm_data.has_key("roll_rate"))
        self.assertAlmostEqual(fdm_data["roll_rate"], mock_fdm_datagram.roll_rate, 3)

        self.assertTrue(fdm_data.has_key("pitch_rate"))
        self.assertAlmostEqual(fdm_data["pitch_rate"], mock_fdm_datagram.pitch_rate, 3)

        self.assertTrue(fdm_data.has_key("yaw_rate"))
        self.assertAlmostEqual(fdm_data["yaw_rate"], mock_fdm_datagram.yaw_rate, 3)

        self.assertTrue(fdm_data.has_key("temperature"))
        self.assertAlmostEqual(fdm_data["temperature"], mock_fdm_datagram.temperature, 3)

        self.assertTrue(fdm_data.has_key("static_pressure"))
        self.assertAlmostEqual(fdm_data["static_pressure"], mock_fdm_datagram.static_pressure, 3)

        self.assertTrue(fdm_data.has_key("total_pressure"))
        self.assertAlmostEqual(fdm_data["total_pressure"], mock_fdm_datagram.total_pressure, 3)

        self.assertTrue(fdm_data.has_key("roll"))
        self.assertAlmostEqual(fdm_data["roll"], mock_fdm_datagram.roll, 3)

        self.assertTrue(fdm_data.has_key("pitch"))
        self.assertAlmostEqual(fdm_data["pitch"], mock_fdm_datagram.pitch, 3)

        self.assertTrue(fdm_data.has_key("thrust"))
        self.assertAlmostEqual(fdm_data["thrust"], mock_fdm_datagram.thrust, 3)

        self.assertTrue(fdm_data.has_key("aileron"))
        self.assertAlmostEqual(fdm_data["aileron"], mock_fdm_datagram.aileron, 3)

        self.assertTrue(fdm_data.has_key("elevator"))
        self.assertAlmostEqual(fdm_data["elevator"], mock_fdm_datagram.elevator, 3)

        self.assertTrue(fdm_data.has_key("rudder"))
        self.assertAlmostEqual(fdm_data["rudder"], mock_fdm_datagram.rudder, 3)

        self.assertTrue(fdm_data.has_key("throttle"))
        self.assertAlmostEqual(fdm_data["throttle"], mock_fdm_datagram.throttle, 3)

def isclose(number_1, number_2, tolerance):
    d = math.fabs(number_1 - number_2)
    
    if d > tolerance:
        return False
    
    return True

class FDMDataMatcher(object):
    def __eq__(self, fdm_data):
        mock_fdm_data_datagram = MockFDMDataDatagram()

        if len(fdm_data) != 22:
            return False

        if not fdm_data.has_key("time"): return False
        if not isclose(fdm_data["time"], mock_fdm_data_datagram.simulation_time, 0.001): return False

        if not fdm_data.has_key("latitude"): return False
        if not isclose(fdm_data["latitude"], mock_fdm_data_datagram.latitude, 0.001): return False

        if not fdm_data.has_key("longitude"): return False
        if not isclose(fdm_data["longitude"], mock_fdm_data_datagram.longitude, 0.001): return False

        if not fdm_data.has_key("altitude"): return False
        if not isclose(fdm_data["altitude"], mock_fdm_data_datagram.altitude, 0.001): return False

        if not fdm_data.has_key("airspeed"): return False
        if not isclose(fdm_data["airspeed"], mock_fdm_data_datagram.airspeed, 0.001): return False

        if not fdm_data.has_key("heading"): return False
        if not isclose(fdm_data["heading"], mock_fdm_data_datagram.heading, 0.001): return False

        if not fdm_data.has_key("x_acceleration"): return False
        if not isclose(fdm_data["x_acceleration"], mock_fdm_data_datagram.x_acceleration, 0.001): return False

        if not fdm_data.has_key("y_acceleration"): return False
        if not isclose(fdm_data["y_acceleration"], mock_fdm_data_datagram.y_acceleration, 0.001): return False

        if not fdm_data.has_key("z_acceleration"): return False
        if not isclose(fdm_data["z_acceleration"], mock_fdm_data_datagram.z_acceleration, 0.001): return False

        if not fdm_data.has_key("roll_rate"): return False
        if not isclose(fdm_data["roll_rate"], mock_fdm_data_datagram.roll_rate, 0.001): return False

        if not fdm_data.has_key("pitch_rate"): return False
        if not isclose(fdm_data["pitch_rate"], mock_fdm_data_datagram.pitch_rate, 0.001): return False

        if not fdm_data.has_key("yaw_rate"): return False
        if not isclose(fdm_data["yaw_rate"], mock_fdm_data_datagram.yaw_rate, 0.001): return False

        if not fdm_data.has_key("temperature"): return False
        if not isclose(fdm_data["temperature"], mock_fdm_data_datagram.temperature, 0.001): return False

        if not fdm_data.has_key("static_pressure"): return False
        if not isclose(fdm_data["static_pressure"], mock_fdm_data_datagram.static_pressure, 0.001): return False

        if not fdm_data.has_key("total_pressure"): return False
        if not isclose(fdm_data["total_pressure"], mock_fdm_data_datagram.total_pressure, 0.001): return False

        if not fdm_data.has_key("roll"): return False
        if not isclose(fdm_data["roll"], mock_fdm_data_datagram.roll, 0.001): return False

        if not fdm_data.has_key("pitch"): return False
        if not isclose(fdm_data["pitch"], mock_fdm_data_datagram.pitch, 0.001): return False

        if not fdm_data.has_key("thrust"): return False
        if not isclose(fdm_data["thrust"], mock_fdm_data_datagram.thrust, 0.001): return False

        if not fdm_data.has_key("aileron"): return False
        if not isclose(fdm_data["aileron"], mock_fdm_data_datagram.aileron, 0.001): return False

        if not fdm_data.has_key("elevator"): return False
        if not isclose(fdm_data["elevator"], mock_fdm_data_datagram.elevator, 0.001): return False

        if not fdm_data.has_key("rudder"): return False
        if not isclose(fdm_data["rudder"], mock_fdm_data_datagram.rudder, 0.001): return False

        if not fdm_data.has_key("throttle"): return False
        if not isclose(fdm_data["throttle"], mock_fdm_data_datagram.throttle, 0.001): return False

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

        expected_datagram = struct.pack("!ffff", 0.1, 0.2, 0.3, 0.4)

        protocol.send_datagram.assert_called_once_with(expected_datagram)