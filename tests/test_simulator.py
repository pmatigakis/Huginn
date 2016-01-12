import pkg_resources
from unittest import TestCase
import inspect
from os import path

from mock.mock import MagicMock

import huginn
from huginn.aircraft import Aircraft
from huginn.simulator import Simulator
from huginn.fdm import create_fdmexec
from huginn import configuration

from mockObjects import MockFDMExec

class TestSimulator(TestCase):
    def test_run_with_real_fdmexec(self):
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdmexec = create_fdmexec(huginn_data_path, "Rascal", configuration.DT)

        aircraft = Aircraft(fdmexec)

        self.assertIsNotNone(fdmexec)

        simulator = Simulator(fdmexec, aircraft)

        start_time = simulator.simulation_time

        simulator.resume()
        
        #run_result = aircraft.run()
        simulator.run()

        self.assertAlmostEqual(simulator.simulation_time,
                               start_time + fdmexec.GetDeltaT(),
                               6)

    def test_run(self):
        fdmexec = MockFDMExec()
        fdmexec.ProcessMessage = MagicMock()
        fdmexec.CheckIncrementalHold = MagicMock()
        fdmexec.Run = MagicMock()
        
        aircraft = Aircraft(fdmexec)
        aircraft.run = MagicMock()
        
        simulator = Simulator(fdmexec, aircraft)
        
        simulator.run()
        
        fdmexec.ProcessMessage.assert_called_once_with()
        fdmexec.CheckIncrementalHold.assert_called_once_with()
        fdmexec.Run.assert_called_once_with()
        aircraft.run.assert_called_once_with()

    def test_reset(self):
        fdmexec = MockFDMExec()
        fdmexec.ResetToInitialConditions = MagicMock()
        fdmexec.Run = MagicMock()
        
        aircraft = Aircraft(fdmexec)
        aircraft.run = MagicMock()
        
        aircraft.controls.aileron = 0.7
        aircraft.controls.elevator = 0.7
        aircraft.controls.rudder = 0.7
        aircraft.controls.throttle = 0.7
        
        simulator = Simulator(fdmexec, aircraft)
        
        simulator.reset()
        
        fdmexec.ResetToInitialConditions.assert_called_once_with(0)
        fdmexec.Run.assert_called_once_with()
        aircraft.run.assert_called_once_with()
        
        self.assertAlmostEqual(aircraft.controls.aileron, 0.0, 3)
        self.assertAlmostEqual(aircraft.controls.rudder, 0.0, 3)
        self.assertAlmostEqual(aircraft.controls.throttle, 0.2, 3)
        self.assertAlmostEqual(aircraft.controls.elevator, 0.0, 3)

    def test_step(self):
        fdmexec = MockFDMExec()
        fdmexec.ProcessMessage = MagicMock()
        fdmexec.CheckIncrementalHold = MagicMock()
        fdmexec.Run = MagicMock()
        
        aircraft = Aircraft(fdmexec)
        aircraft.run = MagicMock()
        
        simulator = Simulator(fdmexec, aircraft)
        
        simulator.step()
        
        fdmexec.ProcessMessage.assert_called_once_with()
        fdmexec.CheckIncrementalHold.assert_called_once_with()
        fdmexec.Run.assert_called_once_with()
        aircraft.run.assert_called_once_with()

    def test_run_for(self):
        fdmexec = MockFDMExec()
        fdmexec.ProcessMessage = MagicMock()
        fdmexec.CheckIncrementalHold = MagicMock()
        
        aircraft = Aircraft(fdmexec)
        aircraft.run = MagicMock()
        
        simulator = Simulator(fdmexec, aircraft)
        
        time_to_run = 1.0
        
        start_time = simulator.simulation_time
        expected_end_time = start_time + time_to_run
        
        simulator.run_for(time_to_run)
        
        self.assertAlmostEqual(expected_end_time, simulator.simulation_time, 3)
        
        fdmexec.ProcessMessage.assert_any_call()
        fdmexec.CheckIncrementalHold.assert_any_call()
        aircraft.run.assert_any_call()
