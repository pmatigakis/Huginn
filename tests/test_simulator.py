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
        huginn_path = inspect.getfile(huginn)
        huginn_data_path = path.join(path.dirname(huginn_path), "data")

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
