from unittest import TestCase
import os

from huginn.simulator import Simulator
from huginn.fdm import create_aircraft_model, create_fdmexec
from huginn import configuration

class TestSimulator(TestCase):
    def test_run(self):
        jsbsim_path = os.environ.get("JSBSIM_HOME", None)

        if not jsbsim_path:
            self.fail("Environment variable JSBSIM_HOME is not set")

        fdmexec = create_fdmexec(jsbsim_path, configuration.DT)

        aircraft = create_aircraft_model(fdmexec, "c172p")
        self.assertIsNotNone(aircraft)

        simulator = Simulator(fdmexec, aircraft)

        initial_condition_valid = simulator.set_initial_conditions(configuration.INITIAL_LATITUDE,
                                                                   configuration.INITIAL_LONGITUDE,
                                                                   600.0,
                                                                   46.0,
                                                                   configuration.INITIAL_HEADING)

        self.assertTrue(initial_condition_valid)

        start_time = simulator.simulation_time

        simulator.resume()
        
        #run_result = aircraft.run()
        run_result = simulator.run()
        self.assertTrue(run_result)

        self.assertAlmostEqual(simulator.simulation_time,
                               start_time + configuration.DT,
                               6)
