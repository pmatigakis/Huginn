from unittest import TestCase

from mock.mock import MagicMock

from huginn.aircraft import Aircraft
from huginn.simulator import Simulator
from huginn.fdm import FDMBuilder
from huginn import configuration

class TestSimulator(TestCase):
    def test_run_with_real_fdmexec(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm = fdm_builder.create_fdm()

        self.assertIsNotNone(fdm)

        aircraft = Aircraft()

        simulator = Simulator(fdm, aircraft)

        start_time = simulator.simulation_time

        simulator.resume()
        
        #run_result = aircraft.run()
        simulator.run()

        self.assertAlmostEqual(simulator.simulation_time,
                               start_time + configuration.DT,
                               6)

    def test_run(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm = fdm_builder.create_fdm()
        
        fdm.update_aircraft = MagicMock()
        
        aircraft = Aircraft()
        
        simulator = Simulator(fdm, aircraft)
        
        result = simulator.run()
        
        self.assertTrue(result)
        fdm.update_aircraft.assert_called_once_with(aircraft)

    def test_reset(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm = fdm_builder.create_fdm()
        
        aircraft = Aircraft()
        
        aircraft.controls.aileron = 0.7
        aircraft.controls.elevator = 0.7
        aircraft.controls.rudder = 0.7
        aircraft.controls.throttle = 0.7
        
        simulator = Simulator(fdm, aircraft)
        
        result = simulator.reset()
        
        self.assertTrue(result)
        self.assertAlmostEqual(aircraft.controls.aileron, 0.0, 3)
        self.assertAlmostEqual(aircraft.controls.rudder, 0.0, 3)
        self.assertAlmostEqual(aircraft.controls.throttle, 0.0, 3)
        self.assertAlmostEqual(aircraft.controls.elevator, 0.0, 3)

    def test_step(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm = fdm_builder.create_fdm()
        
        fdm.update_aircraft = MagicMock()
        
        aircraft = Aircraft()
        
        simulator = Simulator(fdm, aircraft)
        
        result = simulator.step()

        self.assertTrue(result)

        fdm.update_aircraft.assert_called_once_with(aircraft)

    def test_run_for(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm = fdm_builder.create_fdm()
        
        fdm.update_aircraft = MagicMock()
        
        aircraft = Aircraft()
        
        simulator = Simulator(fdm, aircraft)
        
        time_to_run = 1.0
        
        start_time = simulator.simulation_time
        expected_end_time = start_time + time_to_run
        
        result = simulator.run_for(time_to_run)

        self.assertTrue(result)
        self.assertAlmostEqual(expected_end_time, simulator.simulation_time, 3)
        
        fdm.update_aircraft.assert_any_call(aircraft)
