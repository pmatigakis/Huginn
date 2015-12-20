from unittest import TestCase
import inspect
from os import path

import huginn
from huginn.aircraft import Aircraft
from huginn.simulator import Simulator
from huginn.fdm import create_fdmexec
from huginn import configuration

class TestSimulator(TestCase):
    def test_run(self):
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
