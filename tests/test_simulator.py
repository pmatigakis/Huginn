import pkg_resources
from unittest import TestCase

from mock.mock import MagicMock

from huginn.aircraft import Aircraft
from huginn.simulator import Simulator
from huginn.fdm import create_fdmexec
from huginn import configuration

class TestSimulator(TestCase):
    def test_run_with_real_fdmexec(self):
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdm = create_fdmexec(huginn_data_path, "Rascal", configuration.DT)

        self.assertIsNotNone(fdm)

        aircraft = Aircraft(fdm)

        simulator = Simulator(fdm, aircraft)

        start_time = simulator.simulation_time

        simulator.resume()
        
        #run_result = aircraft.run()
        simulator.run()

        self.assertAlmostEqual(simulator.simulation_time,
                               start_time + configuration.DT,
                               6)

    def test_run(self):
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdm = create_fdmexec(huginn_data_path, "Rascal", configuration.DT)
        
        aircraft = Aircraft(fdm)
        aircraft.run = MagicMock()
        
        simulator = Simulator(fdm, aircraft)
        
        simulator.run()
        
        aircraft.run.assert_called_once_with()

    def test_reset(self):
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdm = create_fdmexec(huginn_data_path, "Rascal", configuration.DT)
        
        aircraft = Aircraft(fdm)
        aircraft.run = MagicMock()
        
        aircraft.controls.aileron = 0.7
        aircraft.controls.elevator = 0.7
        aircraft.controls.rudder = 0.7
        aircraft.controls.throttle = 0.7
        
        simulator = Simulator(fdm, aircraft)
        
        simulator.reset()

        aircraft.run.assert_called_once_with()
        
        self.assertAlmostEqual(aircraft.controls.aileron, 0.0, 3)
        self.assertAlmostEqual(aircraft.controls.rudder, 0.0, 3)
        self.assertAlmostEqual(aircraft.controls.throttle, 0.0, 3)
        self.assertAlmostEqual(aircraft.controls.elevator, 0.0, 3)

    def test_step(self):
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdm = create_fdmexec(huginn_data_path, "Rascal", configuration.DT)
        
        aircraft = Aircraft(fdm)
        aircraft.run = MagicMock()
        
        simulator = Simulator(fdm, aircraft)
        
        simulator.step()

        aircraft.run.assert_called_once_with()

    def test_run_for(self):
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdm = create_fdmexec(huginn_data_path, "Rascal", configuration.DT)
        
        aircraft = Aircraft(fdm)
        aircraft.run = MagicMock()
        
        simulator = Simulator(fdm, aircraft)
        
        time_to_run = 1.0
        
        start_time = simulator.simulation_time
        expected_end_time = start_time + time_to_run + configuration.DT
        
        simulator.run_for(time_to_run)
        
        self.assertAlmostEqual(expected_end_time, simulator.simulation_time, 3)
        
        aircraft.run.assert_any_call()
