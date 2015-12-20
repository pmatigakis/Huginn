from unittest import TestCase
import os

from huginn.fdm import create_fdmexec
from huginn import configuration

class TestCreateFDMExec(TestCase):
    def test_create_fdmexec(self):
        jsbsim_path = os.environ.get("JSBSIM_HOME", None)

        fdmexec = create_fdmexec(jsbsim_path, configuration.DT)

        self.assertIsNotNone(fdmexec)
