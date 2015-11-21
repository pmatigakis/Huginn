from unittest import TestCase
import os

from huginn.fdm import create_aircraft_model
from huginn import configuration

class TestCreateFDMModel(TestCase):
    def test_fail_to_create_fdm_model_with_unknown_name(self):
        fdm_model = create_aircraft_model("unknown fdm model", "unknown aircraft", 0.01)

        self.assertIsNone(fdm_model)

class TestJSBSimModelCreation(TestCase):
    def test_create_jsbsim_aircraft_model(self):
        jsbsim_path = os.environ.get("JSBSIM_HOME", None)

        if not jsbsim_path:
            self.fail("Environment variable JSBSIM_HOME is not set")

        aircraft = create_aircraft_model(jsbsim_path, "737", configuration.DT)

        self.assertIsNotNone(aircraft)

class TestJSBSimFDMModel(TestCase): 
    def test_run(self):
        jsbsim_path = os.environ.get("JSBSIM_HOME", None)

        if not jsbsim_path:
            self.fail("Environment variable JSBSIM_HOME is not set")

        aircraft = create_aircraft_model(jsbsim_path, "737", configuration.DT)
        self.assertIsNotNone(aircraft)

        aircraft.set_initial_conditions(configuration.INITIAL_LATITUDE,
                                         configuration.INITIAL_LONGITUDE,
                                         10000.0,
                                         200.0,
                                         configuration.INITIAL_HEADING)

        start_time = aircraft.fdmexec.GetSimTime()
        
        run_result = aircraft.run()
        self.assertTrue(run_result)

        self.assertAlmostEqual(aircraft.fdmexec.GetSimTime(),
                               start_time + configuration.DT,
                               6)
