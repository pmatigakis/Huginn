import struct
from unittest import TestCase
from os import path
import inspect

from huginn_jsbsim import FGFDMExec
from mock import MagicMock

import huginn
from huginn.protocols import FDMDataProtocol, FDMDataRequest,  FDMDataResponse,  FDM_DATA_COMMAND, ERROR_CODE,\
    FDM_DATA_RESPONCE_OK, ControlsProtocol

def get_fdmexec():
    package_filename = inspect.getfile(huginn)
    package_path = path.dirname(package_filename)
    
    fdmexec = FGFDMExec()
    
    fdmexec.set_root_dir(package_path + "/data/")
    fdmexec.set_aircraft_path("aircraft")
    fdmexec.set_engine_path("engine")
    fdmexec.set_systems_path("systems")

    fdmexec.set_dt(1.0/60.0)

    fdmexec.load_model("c172p")

    fdmexec.load_ic("reset01")

    fdmexec.set_property_value("fcs/throttle-cmd-norm", 0.65)
    fdmexec.set_property_value("fcs/mixture-cmd-norm", 0.87)
    fdmexec.set_property_value("propulsion/magneto_cmd", 3.0)
    fdmexec.set_property_value("propulsion/starter_cmd", 1.0)

    initial_condition_result = fdmexec.run_ic()

    if not initial_condition_result:
        print("Failed to run initial condition")
        exit(-1)

    running = fdmexec.run()
    while running and fdmexec.get_sim_time() < 0.1:
        fdmexec.process_message()
        fdmexec.check_incremental_hold()

        running = fdmexec.run()
        
    result = fdmexec.trim()    
    if not result:
        print("Failed to trim the aircraft")
        exit(-1)
        
    return fdmexec

class TestFDMDataProtocol(TestCase):
    def test_decode_request(self):
        fdmexec = get_fdmexec()
        
        fdm_data_protocol = FDMDataProtocol(fdmexec)
        
        request_datagram = struct.pack("!c", chr(FDM_DATA_COMMAND))
        host = "127.0.0.1"
        port = 12345
        
        request = fdm_data_protocol.decode_request(request_datagram, host, port)
        
        self.assertIsInstance(request, FDMDataRequest)
        self.assertEqual(request.host, host)
        self.assertEqual(request.port, port)
        self.assertEqual(request.command, FDM_DATA_COMMAND)
        
    def test_return_error_code_on_invalid_request_datagram(self):
        fdmexec = get_fdmexec()
        
        fdm_data_protocol = FDMDataProtocol(fdmexec)
        
        fdm_data_protocol.transmit_error_code = MagicMock()
        
        request_datagram = struct.pack("!cc", chr(FDM_DATA_COMMAND), chr(0x00))
        host = "127.0.0.1"
        port = 12345
        
        fdm_data_protocol.datagramReceived(request_datagram, (host, port))
        
        fdm_data_protocol.transmit_error_code.assert_called_once_with(ERROR_CODE, host, port)
        
    def test_return_error_code_on_invalid_request_command(self):
        fdmexec = get_fdmexec()
        
        fdm_data_protocol = FDMDataProtocol(fdmexec)
        
        fdm_data_protocol.transmit_error_code = MagicMock()
        
        request_datagram = struct.pack("!cc", chr(0x50), chr(0x00))
        host = "127.0.0.1"
        port = 12345
        
        fdm_data_protocol.datagramReceived(request_datagram, (host, port))
        
        fdm_data_protocol.transmit_error_code.assert_called_once_with(ERROR_CODE, host, port)

class TestFDMDataResponse(TestCase):
    def test_encode_response(self):
        fdm_data_request = FDMDataRequest("127.0.0.1", 12345, FDM_DATA_COMMAND)
        
        fdm_property_values = [1.0, 2.0, 3.0]
        
        fdm_data_response = FDMDataResponse(fdm_data_request, fdm_property_values)
        
        encoded_response = fdm_data_response.encode_response()
        
        decoded_reponse = struct.unpack("!cfff", encoded_response)
        
        self.assertEqual(ord(decoded_reponse[0]), FDM_DATA_RESPONCE_OK)
        self.assertAlmostEqual(decoded_reponse[1], 1.0)
        self.assertAlmostEqual(decoded_reponse[2], 2.0)
        self.assertAlmostEqual(decoded_reponse[3], 3.0)
        
class TestControlsProtocol(TestCase):
    def test_datagram_received(self):
        fdmexec = get_fdmexec()
        
        controls_protocol = ControlsProtocol(fdmexec)
        
        aileron = 0.1
        elevator = 0.2
        rudder = 0.3
        throttle = 0.4
        
        controls_datagram = struct.pack("!ffff", aileron, elevator, rudder, throttle)
        
        host = "127.0.0.1"
        port = 12345
        
        controls_protocol.datagramReceived(controls_datagram, (host, port))
                
        self.assertAlmostEqual(fdmexec.get_property_value("fcs/aileron-cmd-norm"), aileron, 3)                  
        self.assertAlmostEqual(fdmexec.get_property_value("fcs/elevator-cmd-norm"), elevator, 3)
        self.assertAlmostEqual(fdmexec.get_property_value("fcs/rudder-cmd-norm"), rudder, 3)
        self.assertAlmostEqual(fdmexec.get_property_value("fcs/throttle-cmd-norm"), throttle, 3)