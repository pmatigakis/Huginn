from unittest import TestCase
from os import path
import inspect

from flightsimlib import FGFDMExec

import huginn
from huginn.protocols import FDMDataEncoder, FDMDataDecoder
from huginn.fdm import fdm_data_properties

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

class EncodingAndDecodingFDMDataTests(TestCase):
    def test_encode_and_decode_fdm_data(self):
        fdmexec = get_fdmexec()
        
        fdm_data_encoder = FDMDataEncoder(fdmexec)
        
        encoded_fdm_data = fdm_data_encoder.encode_fdm_data(fdm_data_properties)
        
        fdm_data_decoder = FDMDataDecoder()
        
        decoded_fdm_data = fdm_data_decoder.decode_fdm_data(encoded_fdm_data, fdm_data_properties)
        
        for fdm_property in fdm_data_properties:
            self.assertAlmostEqual(decoded_fdm_data[fdm_property], fdmexec.get_property_value(fdm_property), 3)