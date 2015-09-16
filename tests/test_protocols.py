import struct
from unittest import TestCase

from mock import MagicMock

from test_common import get_fdmexec

from huginn.protocols import FDMDataProtocol, FDMDataRequest,  FDMDataResponse,  ERROR_CODE,\
    FDM_DATA_RESPONCE_OK, ControlsProtocol, GPS_DATA_REQUEST, FDMDataGPSResponseDecoder,\
    ACCELEROMETER_DATA_REQUEST, GYROSCOPE_DATA_REQUEST,\
    MAGNETOMETER_DATA_REQUEST, THERMOMETER_DATA_REQUEST, PITOT_TUBE_DATA_REQUEST,\
    STATIC_PRESSURE_DATA_REQUEST, INS_DATA_REQUEST
from huginn.aircraft import Aircraft

class TestFDMDataGPSResponseDecoder(TestCase):
    def setUp(self):
        self.fdmexec = get_fdmexec()
    
    def test_decode_response(self):
        aircraft = Aircraft(self.fdmexec) 
  
        request = FDMDataRequest("127.0.0.1", 12345, GPS_DATA_REQUEST)
          
        fdm_data_protocol = FDMDataProtocol(aircraft)
          
        response = fdm_data_protocol.create_gps_data_response(request)
          
        encoded_response = response.encode_response()
          
        gps_data_decoder = FDMDataGPSResponseDecoder()
          
        response_code, command, gps_data = gps_data_decoder.decode_response(encoded_response)
          
        self.assertEqual(response_code, FDM_DATA_RESPONCE_OK)
        self.assertEqual(command, GPS_DATA_REQUEST)
          
        self.assertTrue(gps_data.has_key("latitude"))
        self.assertTrue(gps_data.has_key("longitude"))
        self.assertTrue(gps_data.has_key("airspeed"))
        self.assertTrue(gps_data.has_key("altitude"))
        self.assertTrue(gps_data.has_key("heading"))
          
        self.assertAlmostEqual(gps_data["latitude"], aircraft.gps.latitude, 3)
        self.assertAlmostEqual(gps_data["longitude"], aircraft.gps.longitude, 3)
        self.assertAlmostEqual(gps_data["airspeed"], aircraft.gps.airspeed, 3)
        self.assertAlmostEqual(gps_data["altitude"], aircraft.gps.altitude, 3)
        self.assertAlmostEqual(gps_data["heading"], aircraft.gps.heading, 3)

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