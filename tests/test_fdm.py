from unittest import TestCase
import os

from huginn.fdm import JSBSimFDMModelCreator
from huginn import configuration

class TestJSBSimFDMModelCreator(TestCase):
    def test_create_fdm_model(self):
        jsbsim_path = os.environ.get("JSBSIM_HOME", None)

        if not jsbsim_path:
            self.fail("Environment variable JSBSIM_HOME is not set")

        fdm_model_creator = JSBSimFDMModelCreator(jsbsim_path,
                                                  configuration.DT,
                                                  configuration.INITIAL_LATITUDE,
                                                  configuration.INITIAL_LONGITUDE,
                                                  configuration.INITIAL_ALTITUDE,
                                                  configuration.INITIAL_AIRSPEED,
                                                  configuration.INITIAL_HEADING)

        fdm_model = fdm_model_creator.create_fdm_model()

        self.assertIsNotNone(fdm_model)

class TestJSBSimFDMModelAdapter(TestCase):
    def test_run(self):
        jsbsim_path = os.environ.get("JSBSIM_HOME", None)

        if not jsbsim_path:
            self.fail("Environment variable JSBSIM_HOME is not set")

        fdm_model_creator = JSBSimFDMModelCreator(jsbsim_path,
                                                  configuration.DT,
                                                  configuration.INITIAL_LATITUDE,
                                                  configuration.INITIAL_LONGITUDE,
                                                  configuration.INITIAL_ALTITUDE,
                                                  configuration.INITIAL_AIRSPEED,
                                                  configuration.INITIAL_HEADING)

        fdm_model = fdm_model_creator.create_fdm_model()

        self.assertIsNotNone(fdm_model)

        run_result = fdm_model.run()
        self.assertTrue(run_result)

        start_time = fdm_model.get_property_value("simulation/sim-time-sec")

        self.assertAlmostEqual(start_time, configuration.DT, 6)

        run_result = fdm_model.run()
        self.assertTrue(run_result)

        self.assertAlmostEqual(fdm_model.get_property_value("simulation/sim-time-sec"),
                               start_time + configuration.DT,
                               6)
