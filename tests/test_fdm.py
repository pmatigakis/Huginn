from unittest import TestCase
import os

from huginn.fdm import create_aircraft_model, create_fdmexec
from huginn import configuration

class TestCreateFDMExec(TestCase):
    def test_create_fdmexec(self):
        jsbsim_path = os.environ.get("JSBSIM_HOME", None)

        fdmexec = create_fdmexec(jsbsim_path, configuration.DT)

        self.assertIsNotNone(fdmexec)

class TestCreateFDMModel(TestCase):
    def test_fail_to_create_fdm_model_with_unknown_name(self):
        jsbsim_path = os.environ.get("JSBSIM_HOME", None)

        if not jsbsim_path:
            self.fail("Environment variable JSBSIM_HOME is not set")

        fdmexec = create_fdmexec(jsbsim_path, configuration.DT)

        fdm_model = create_aircraft_model(fdmexec, "unknown aircraft")

        self.assertIsNone(fdm_model)

class TestJSBSimModelCreation(TestCase):
    def test_create_jsbsim_aircraft_model(self):
        jsbsim_path = os.environ.get("JSBSIM_HOME", None)

        if not jsbsim_path:
            self.fail("Environment variable JSBSIM_HOME is not set")

        fdmexec = create_fdmexec(jsbsim_path, configuration.DT)

        aircraft = create_aircraft_model(fdmexec, "737")

        self.assertIsNotNone(aircraft)
