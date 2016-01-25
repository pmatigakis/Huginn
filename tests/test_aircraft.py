import pkg_resources
from unittest import TestCase
import math

from huginn.aircraft import Controls, Engine, GPS, Accelerometer, Gyroscope,\
                            Thermometer, PressureSensor, PitotTube
from huginn.unit_conversions import convert_feet_to_meters 
from huginn.unit_conversions import convert_feet_sec_squared_to_meters_sec_squared,\
                                    convert_radians_sec_to_degrees_sec
from huginn.unit_conversions import convert_rankine_to_kelvin, convert_psf_to_pascal,\
                                    convert_libra_to_newtons
from huginn.fdm import FDMBuilder
from huginn import configuration

from mock.mock import MagicMock

class TestControls(TestCase):    
    def test_set_aileron(self):
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm = fdm_builder.create_fdm()
        
        controls = Controls()
        
        fdm.set_aircraft_controls(0.678, 0.0, 0.0, 0.0)
        
        fdm.update_aircraft_controls(controls)
        
        self.assertAlmostEqual(controls.aileron, 0.678, 3)
            
    def test_set_elevator(self):
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm = fdm_builder.create_fdm()
        
        controls = Controls()
        
        fdm.set_aircraft_controls(0.0, 0.378, 0.0, 0.0)
        
        fdm.update_aircraft_controls(controls)
        
        self.assertAlmostEqual(controls.elevator, 0.378, 3)
        
    def test_set_rudder(self):
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm = fdm_builder.create_fdm()
        
        controls = Controls()
        
        fdm.set_aircraft_controls(0.0, 0.0, 0.178, 0.0)
        
        fdm.update_aircraft_controls(controls)
        
        self.assertAlmostEqual(controls.rudder, 0.178, 0.0)
    
    def test_set_throttle(self):
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm = fdm_builder.create_fdm()
        
        controls = Controls()
        
        fdm.set_aircraft_controls(0.0, 0.0, 0.0, 0.198)
        
        fdm.update_aircraft_controls(controls)
        
        self.assertAlmostEqual(controls.throttle, 0.198)
