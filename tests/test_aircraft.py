from unittest import TestCase
import math

from huginn.aircraft import Aircraft, Engine
from huginn.fdm import FDMBuilder
from huginn import configuration
from huginn.unit_conversions import convert_libra_to_newtons

class EngineTests(TestCase):
    def test_engine(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        engine = Engine(fdmexec)

        self.assertAlmostEqual(engine.thrust, convert_libra_to_newtons(fdmexec.GetPropulsion().GetEngine(0).GetThruster().GetThrust()))
        self.assertAlmostEqual(engine.throttle, fdmexec.GetFCS().GetThrottleCmd(0))

class TestControls(TestCase):
    def test_set_aileron(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()
        
        aircraft = Aircraft(fdmexec)
        
        fdmexec.GetFCS().SetDaCmd(0.678)
        
        self.assertAlmostEqual(aircraft.controls.aileron, 0.678, 3)
            
    def test_set_elevator(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()
        
        aircraft = Aircraft(fdmexec)
        
        fdmexec.GetFCS().SetDeCmd(0.378)
        
        self.assertAlmostEqual(aircraft.controls.elevator, 0.378, 3)
        
    def test_set_rudder(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()
        
        aircraft = Aircraft(fdmexec)
        
        fdmexec.GetFCS().SetDrCmd(0.178)
        
        self.assertAlmostEqual(aircraft.controls.rudder, 0.178, 0.0)
    
    def test_set_throttle(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()
        
        aircraft = Aircraft(fdmexec)
        
        fdmexec.GetFCS().SetThrottleCmd(0, 0.198)
        
        self.assertAlmostEqual(aircraft.controls.throttle, 0.198)
