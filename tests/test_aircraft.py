from unittest import TestCase

from huginn.aircraft import Controls, Aircraft
from huginn.fdm import FDMBuilder
from huginn import configuration

class TestControls(TestCase):    
    def test_set_aileron(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()
        
        aircraft = Aircraft()
        
        fdmexec.GetFCS().SetDaCmd(0.678)
        
        aircraft.update_from_fdmexec(fdmexec)
        
        self.assertAlmostEqual(aircraft.controls.aileron, 0.678, 3)
            
    def test_set_elevator(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()
        
        aircraft = Aircraft()
        
        fdmexec.GetFCS().SetDeCmd(0.378)
        
        aircraft.update_from_fdmexec(fdmexec)
        
        self.assertAlmostEqual(aircraft.controls.elevator, 0.378, 3)
        
    def test_set_rudder(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()
        
        aircraft = Aircraft()
        
        fdmexec.GetFCS().SetDrCmd(0.178)
        
        aircraft.update_from_fdmexec(fdmexec)
        
        self.assertAlmostEqual(aircraft.controls.rudder, 0.178, 0.0)
    
    def test_set_throttle(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()
        
        aircraft = Aircraft()
        
        fdmexec.GetFCS().SetThrottleCmd(0, 0.198)
        
        aircraft.update_from_fdmexec(fdmexec)
        
        self.assertAlmostEqual(aircraft.controls.throttle, 0.198)
