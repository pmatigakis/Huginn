from unittest import TestCase

from huginn.aircraft import Controls
from huginn.fdm import FDMBuilder
from huginn import configuration

class TestControls(TestCase):    
    def test_set_aileron(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm = fdm_builder.create_fdm()
        
        controls = Controls()
        
        fdm.set_aircraft_controls(0.678, 0.0, 0.0, 0.0)
        
        fdm.update_aircraft_controls(controls)
        
        self.assertAlmostEqual(controls.aileron, 0.678, 3)
            
    def test_set_elevator(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm = fdm_builder.create_fdm()
        
        controls = Controls()
        
        fdm.set_aircraft_controls(0.0, 0.378, 0.0, 0.0)
        
        fdm.update_aircraft_controls(controls)
        
        self.assertAlmostEqual(controls.elevator, 0.378, 3)
        
    def test_set_rudder(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm = fdm_builder.create_fdm()
        
        controls = Controls()
        
        fdm.set_aircraft_controls(0.0, 0.0, 0.178, 0.0)
        
        fdm.update_aircraft_controls(controls)
        
        self.assertAlmostEqual(controls.rudder, 0.178, 0.0)
    
    def test_set_throttle(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm = fdm_builder.create_fdm()
        
        controls = Controls()
        
        fdm.set_aircraft_controls(0.0, 0.0, 0.0, 0.198)
        
        fdm.update_aircraft_controls(controls)
        
        self.assertAlmostEqual(controls.throttle, 0.198)
