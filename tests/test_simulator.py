from unittest import TestCase
import os

from huginn.aircraft import Aircraft
from huginn.simulator import Simulator
from huginn.fdm import create_fdmexec
from huginn import configuration

class TestSimulator(TestCase):
    def test_run(self):
        jsbsim_path = os.environ.get("JSBSIM_HOME", None)

        if not jsbsim_path:
            self.fail("Environment variable JSBSIM_HOME is not set")

        fdmexec = create_fdmexec(jsbsim_path, "/scripts/737_cruise.xml", configuration.DT)

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
