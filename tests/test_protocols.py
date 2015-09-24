import struct
from unittest import TestCase

from mock import MagicMock

from test_common import get_fdmexec

from huginn.protocols import FDMDataProtocol, FDMDataRequest,  FDMDataResponse,  ERROR_CODE,\
    FDM_DATA_RESPONCE_OK, ControlsProtocol, GPS_DATA_REQUEST,\
    ACCELEROMETER_DATA_REQUEST, GYROSCOPE_DATA_REQUEST,\
    MAGNETOMETER_DATA_REQUEST, THERMOMETER_DATA_REQUEST, PITOT_TUBE_DATA_REQUEST,\
    STATIC_PRESSURE_DATA_REQUEST, INS_DATA_REQUEST, SimulatorControl,\
    TelemetryFactory, SIMULATION_PAUSE, SIMULATION_RESET, SIMULATION_RESUME,\
    TelemetryProtocol
from huginn.aircraft import Aircraft

class TestFDMDataProtocol(TestCase):
    def setUp(self):
        self.fdmexec = get_fdmexec() 

    def test_decode_request(self):
        aircraft = Aircraft(self.fdmexec)
              
        fdm_data_protocol = FDMDataProtocol(aircraft)
              
        request_datagram = struct.pack("!c", chr(GPS_DATA_REQUEST))
        host = "127.0.0.1"
        port = 12345
              
        request = fdm_data_protocol.decode_request(request_datagram, host, port)
              
        self.assertIsInstance(request, FDMDataRequest)
        self.assertEqual(request.host, host)
        self.assertEqual(request.port, port)
        self.assertEqual(request.command, GPS_DATA_REQUEST)
          
    def test_return_error_code_on_invalid_request_datagram(self):
        aircraft = Aircraft(self.fdmexec)
               
        fdm_data_protocol = FDMDataProtocol(aircraft)
               
        fdm_data_protocol.transmit_error_code = MagicMock()
               
        request_datagram = struct.pack("!cc", chr(GPS_DATA_REQUEST), chr(0x00))
        host = "127.0.0.1"
        port = 12345
               
        fdm_data_protocol.datagramReceived(request_datagram, (host, port))
               
        fdm_data_protocol.transmit_error_code.assert_called_once_with(ERROR_CODE, host, port)
           
    def test_return_error_code_on_invalid_request_command(self):
        aircraft = Aircraft(self.fdmexec)
           
        fdm_data_protocol = FDMDataProtocol(aircraft)
            
        fdm_data_protocol.transmit_error_code = MagicMock()
            
        request_datagram = struct.pack("!cc", chr(0x50), chr(0x00))
        host = "127.0.0.1"
        port = 12345
            
        fdm_data_protocol.datagramReceived(request_datagram, (host, port))
            
        fdm_data_protocol.transmit_error_code.assert_called_once_with(ERROR_CODE, host, port)
  
    def test_create_gps_data_response(self):
        aircraft = Aircraft(self.fdmexec)
           
        request = FDMDataRequest("127.0.0.1", 12345, GPS_DATA_REQUEST)
           
        fdm_data_protocol = FDMDataProtocol(aircraft)
           
        response = fdm_data_protocol.create_gps_data_response(request)
           
        self.assertEqual(len(response.fdm_property_values), 5)
        self.assertEqual(response.fdm_data_request, request)
           
        self.assertAlmostEqual(response.fdm_property_values[0], aircraft.gps.latitude, 3)
        self.assertAlmostEqual(response.fdm_property_values[1], aircraft.gps.longitude, 3)
        self.assertAlmostEqual(response.fdm_property_values[2], aircraft.gps.altitude, 3)
        self.assertAlmostEqual(response.fdm_property_values[3], aircraft.gps.airspeed, 3)
        self.assertAlmostEqual(response.fdm_property_values[4], aircraft.gps.heading, 3)
  
    def test_create_accelerometer_data_response(self):
        aircraft = Aircraft(self.fdmexec)
           
        request = FDMDataRequest("127.0.0.1", 12345, ACCELEROMETER_DATA_REQUEST)
           
        fdm_data_protocol = FDMDataProtocol(aircraft)
   
        response = fdm_data_protocol.create_accelerometer_data_response(request)
           
        self.assertEqual(len(response.fdm_property_values), 3)
        self.assertEqual(response.fdm_data_request, request)
           
        self.assertAlmostEqual(response.fdm_property_values[0], aircraft.accelerometer.x_acceleration, 3)
        self.assertAlmostEqual(response.fdm_property_values[1], aircraft.accelerometer.y_acceleration, 3)
        self.assertAlmostEqual(response.fdm_property_values[2], aircraft.accelerometer.z_acceleration, 3)
  
    def test_create_gyroscope_data_response(self):
        aircraft = Aircraft(self.fdmexec)
           
        request = FDMDataRequest("127.0.0.1", 12345, GYROSCOPE_DATA_REQUEST)
           
        fdm_data_protocol = FDMDataProtocol(aircraft)
   
        response = fdm_data_protocol.create_gyroscope_data_response(request)
           
        self.assertEqual(len(response.fdm_property_values), 3)
        self.assertEqual(response.fdm_data_request, request)
           
        self.assertAlmostEqual(response.fdm_property_values[0], aircraft.gyroscope.roll_rate, 3)
        self.assertAlmostEqual(response.fdm_property_values[1], aircraft.gyroscope.pitch_rate, 3)
        self.assertAlmostEqual(response.fdm_property_values[2], aircraft.gyroscope.yaw_rate, 3)
  
    def test_create_magnetometer_data_response(self):
        aircraft = Aircraft(self.fdmexec)
           
        request = FDMDataRequest("127.0.0.1", 12345, MAGNETOMETER_DATA_REQUEST)
           
        fdm_data_protocol = FDMDataProtocol(aircraft)
   
        response = fdm_data_protocol.create_magnetometer_data_response(request)
           
        self.assertEqual(len(response.fdm_property_values), 3)
        self.assertEqual(response.fdm_data_request, request)
           
        self.assertAlmostEqual(response.fdm_property_values[0], 0.0, 3)
        self.assertAlmostEqual(response.fdm_property_values[1], 0.0, 3)
        self.assertAlmostEqual(response.fdm_property_values[2], 0.0, 3)
  
    def test_create_thermometer_data_response(self):
        aircraft = Aircraft(self.fdmexec)
           
        request = FDMDataRequest("127.0.0.1", 12345, THERMOMETER_DATA_REQUEST)
           
        fdm_data_protocol = FDMDataProtocol(aircraft)
           
        response = fdm_data_protocol.create_thermometer_data_response(request)
           
        self.assertEqual(len(response.fdm_property_values), 1)
        self.assertEqual(response.fdm_data_request, request)
   
        self.assertAlmostEqual(response.fdm_property_values[0], aircraft.thermometer.temperature, 3)
  
    def test_create_pitot_tube_data_response(self):
        aircraft = Aircraft(self.fdmexec)
           
        request = FDMDataRequest("127.0.0.1", 12345, PITOT_TUBE_DATA_REQUEST)
           
        fdm_data_protocol = FDMDataProtocol(aircraft)
           
        response = fdm_data_protocol.create_pitot_tube_data_response(request)
           
        self.assertEqual(len(response.fdm_property_values), 1)
        self.assertEqual(response.fdm_data_request, request)
   
        self.assertAlmostEqual(response.fdm_property_values[0], aircraft.pitot_tube.pressure, 3)
 
    def test_create_static_pressure_data_response(self):
        aircraft = Aircraft(self.fdmexec)
           
        request = FDMDataRequest("127.0.0.1", 12345, STATIC_PRESSURE_DATA_REQUEST)
           
        fdm_data_protocol = FDMDataProtocol(aircraft)
   
        response = fdm_data_protocol.create_static_pressure_data_response(request)
   
        self.assertEqual(len(response.fdm_property_values), 1)
        self.assertEqual(response.fdm_data_request, request)
   
        self.assertAlmostEqual(response.fdm_property_values[0], aircraft.pressure_sensor.pressure, 3)
      
    def test_create_ins_data_response(self):
        aircraft = Aircraft(self.fdmexec)
            
        request = FDMDataRequest("127.0.0.1", 12345, INS_DATA_REQUEST)
            
        fdm_data_protocol = FDMDataProtocol(aircraft)
            
        response = fdm_data_protocol.create_ins_data_response(request)
    
        self.assertEqual(len(response.fdm_property_values), 7)
        self.assertEqual(response.fdm_data_request, request)
            
        self.assertAlmostEqual(response.fdm_property_values[0], aircraft.inertial_navigation_system.roll, 3)
        self.assertAlmostEqual(response.fdm_property_values[1], aircraft.inertial_navigation_system.pitch, 3)
        self.assertAlmostEqual(response.fdm_property_values[2], aircraft.inertial_navigation_system.heading, 3)
        self.assertAlmostEqual(response.fdm_property_values[3], aircraft.inertial_navigation_system.latitude, 3)
        self.assertAlmostEqual(response.fdm_property_values[4], aircraft.inertial_navigation_system.longitude, 3)
        self.assertAlmostEqual(response.fdm_property_values[5], aircraft.inertial_navigation_system.airspeed, 3)
        self.assertAlmostEqual(response.fdm_property_values[6], aircraft.inertial_navigation_system.altitude, 3)
       
class TestFDMDataResponse(TestCase):
    def test_encode_response(self):
        fdm_data_request = FDMDataRequest("127.0.0.1", 12345, GPS_DATA_REQUEST)
            
        fdm_property_values = [1.0, 2.0, 3.0, 4.0, 5.0]
            
        fdm_data_response = FDMDataResponse(fdm_data_request, fdm_property_values)
            
        encoded_response = fdm_data_response.encode_response()
            
        decoded_reponse = struct.unpack("!ccfffff", encoded_response)
            
        self.assertEqual(ord(decoded_reponse[0]), FDM_DATA_RESPONCE_OK)
        self.assertEqual(ord(decoded_reponse[1]), GPS_DATA_REQUEST)
        self.assertAlmostEqual(decoded_reponse[2], 1.0)
        self.assertAlmostEqual(decoded_reponse[3], 2.0)
        self.assertAlmostEqual(decoded_reponse[4], 3.0)
        self.assertAlmostEqual(decoded_reponse[5], 4.0)
        self.assertAlmostEqual(decoded_reponse[6], 5.0)
           
class TestControlsProtocol(TestCase):
    def setUp(self):
        self.fdmexec = get_fdmexec()
        self.aircraft = Aircraft(self.fdmexec)
                
    def test_datagram_received(self):
        controls_protocol = ControlsProtocol(self.aircraft)
             
        aileron = 0.1
        elevator = 0.2
        rudder = 0.3
        throttle = 0.4
             
        controls_datagram = struct.pack("!ffff", aileron, elevator, rudder, throttle)
             
        host = "127.0.0.1"
        port = 12345
             
        controls_protocol.datagramReceived(controls_datagram, (host, port))
                     
        self.assertAlmostEqual(self.aircraft.controls.aileron, aileron, 3)                  
        self.assertAlmostEqual(self.aircraft.controls.elevator, elevator, 3)
        self.assertAlmostEqual(self.aircraft.controls.rudder, rudder, 3)
        self.assertAlmostEqual(self.aircraft.engine.throttle, throttle, 3)
        
class TestSimulatorControl(TestCase):
    def setUp(self):
        self.fdmexec = get_fdmexec()
    
    def test_reset_simulator(self):
        protocol = SimulatorControl(self.fdmexec)

        self.fdmexec.trim = MagicMock()

        reset_datagram = struct.pack("!c", chr(SIMULATION_RESET))

        protocol.datagramReceived(reset_datagram, ("127.0.0.1", 12345))

        self.fdmexec.trim.assert_called_once_with()

    def test_resume_simulator(self):
        protocol = SimulatorControl(self.fdmexec)

        self.fdmexec.resume = MagicMock()

        reset_datagram = struct.pack("!c", chr(SIMULATION_RESUME))

        protocol.datagramReceived(reset_datagram, ("127.0.0.1", 12345))

        self.fdmexec.resume.assert_called_once_with()

    def test_pause_simulator(self):
        protocol = SimulatorControl(self.fdmexec)

        self.fdmexec.hold = MagicMock()

        reset_datagram = struct.pack("!c", chr(SIMULATION_PAUSE))

        protocol.datagramReceived(reset_datagram, ("127.0.0.1", 12345))

        self.fdmexec.hold.assert_called_once_with()

class TestTelemetryFactory(TestCase):
    def setUp(self):
        self.fdmexec = get_fdmexec()
        self.aircraft = Aircraft(self.fdmexec)

    def test_get_telemetry_data(self):
        factory = TelemetryFactory(self.fdmexec, self.aircraft)
        protocol = TelemetryProtocol(factory)

        telemetry_data = factory.get_telemetry_data()

        self.assertEqual(len(telemetry_data), len(protocol.telemetry_items))

        for item in protocol.telemetry_items:
            self.assertTrue(telemetry_data.has_key(item))

        self.assertAlmostEqual(telemetry_data["time"], self.fdmexec.get_property_value("simulation/sim-time-sec"), 3)
        self.assertAlmostEqual(telemetry_data["dt"], self.fdmexec.get_property_value("simulation/dt"), 3)
        self.assertAlmostEqual(telemetry_data["running"], not self.fdmexec.holding(), 3)
        self.assertAlmostEqual(telemetry_data["latitude"], self.aircraft.gps.latitude, 3)
        self.assertAlmostEqual(telemetry_data["longitude"], self.aircraft.gps.longitude, 3)
        self.assertAlmostEqual(telemetry_data["altitude"], self.aircraft.gps.altitude, 3)
        self.assertAlmostEqual(telemetry_data["airspeed"], self.aircraft.gps.airspeed, 3)
        self.assertAlmostEqual(telemetry_data["heading"], self.aircraft.gps.heading, 3)
        self.assertAlmostEqual(telemetry_data["x_acceleration"], self.aircraft.accelerometer.x_acceleration, 3)
        self.assertAlmostEqual(telemetry_data["y_acceleration"], self.aircraft.accelerometer.y_acceleration, 3)
        self.assertAlmostEqual(telemetry_data["z_acceleration"], self.aircraft.accelerometer.z_acceleration, 3)
        self.assertAlmostEqual(telemetry_data["roll_rate"], self.aircraft.gyroscope.roll_rate, 3)
        self.assertAlmostEqual(telemetry_data["pitch_rate"], self.aircraft.gyroscope.pitch_rate, 3)
        self.assertAlmostEqual(telemetry_data["yaw_rate"], self.aircraft.gyroscope.yaw_rate, 3)
        self.assertAlmostEqual(telemetry_data["temperature"], self.aircraft.thermometer.temperature, 3)
        self.assertAlmostEqual(telemetry_data["static_pressure"], self.aircraft.pressure_sensor.pressure, 3)
        self.assertAlmostEqual(telemetry_data["dynamic_pressure"], self.aircraft.pitot_tube.pressure, 3)
        self.assertAlmostEqual(telemetry_data["roll"], self.aircraft.inertial_navigation_system.roll, 3)
        self.assertAlmostEqual(telemetry_data["pitch"], self.aircraft.inertial_navigation_system.pitch, 3)
        self.assertAlmostEqual(telemetry_data["engine_rpm"], self.aircraft.engine.rpm, 3)
        self.assertAlmostEqual(telemetry_data["engine_thrust"], self.aircraft.engine.thrust, 3)
        self.assertAlmostEqual(telemetry_data["engine_power"], self.aircraft.engine.power, 3)
        self.assertAlmostEqual(telemetry_data["aileron"], self.aircraft.controls.aileron, 3)
        self.assertAlmostEqual(telemetry_data["elevator"], self.aircraft.controls.elevator, 3)
        self.assertAlmostEqual(telemetry_data["rudder"], self.aircraft.controls.rudder, 3)
        self.assertAlmostEqual(telemetry_data["throttle"], self.aircraft.engine.throttle, 3)
