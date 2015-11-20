from unittest import TestCase
import os

from huginn.fdm import create_jsbsim_fdm_model, create_fdmmodel
from huginn import configuration

class TestCreateFDMModel(TestCase):
    def test_fail_to_create_fdm_model_with_unknown_name(self):
        fdm_model = create_fdmmodel("unknown fdm model", "unknown aircraft", 0.01)

        self.assertIsNone(fdm_model)

class TestJSBSimModelCreation(TestCase):
    def test_create_jsbsim_fdm_model(self):
        jsbsim_path = os.environ.get("JSBSIM_HOME", None)

        if not jsbsim_path:
            self.fail("Environment variable JSBSIM_HOME is not set")

        fdm_model = create_jsbsim_fdm_model(jsbsim_path, configuration.DT, "737")

        self.assertIsNotNone(fdm_model)

class TestJSBSimFDMModel(TestCase):
    def test_load_initial_conditions(self):
        jsbsim_path = os.environ.get("JSBSIM_HOME", None)

        if not jsbsim_path:
            self.fail("Environment variable JSBSIM_HOME is not set")

        fdm_model = create_jsbsim_fdm_model(jsbsim_path, configuration.DT, "737")
        self.assertIsNotNone(fdm_model)

        initialization_result = fdm_model.load_initial_conditions(configuration.INITIAL_LATITUDE,
                                                                  configuration.INITIAL_LONGITUDE,
                                                                  configuration.INITIAL_ALTITUDE,
                                                                  configuration.INITIAL_AIRSPEED,
                                                                  configuration.INITIAL_HEADING)

        self.assertTrue(initialization_result)
 
    def test_run(self):
        jsbsim_path = os.environ.get("JSBSIM_HOME", None)

        if not jsbsim_path:
            self.fail("Environment variable JSBSIM_HOME is not set")

        fdm_model = create_jsbsim_fdm_model(jsbsim_path, configuration.DT, "737")
        self.assertIsNotNone(fdm_model)

        initialization_result = fdm_model.load_initial_conditions(configuration.INITIAL_LATITUDE,
                                                                  configuration.INITIAL_LONGITUDE,
                                                                  configuration.INITIAL_ALTITUDE,
                                                                  configuration.INITIAL_AIRSPEED,
                                                                  configuration.INITIAL_HEADING)

        self.assertTrue(initialization_result)

        start_time = fdm_model.sim_time

        fdm_model.resume()
        
        run_result = fdm_model.run()
        self.assertTrue(run_result)

        self.assertAlmostEqual(fdm_model.sim_time,
                               start_time + configuration.DT,
                               6)
