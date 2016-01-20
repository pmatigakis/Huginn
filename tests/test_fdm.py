import pkg_resources
from unittest import TestCase

from huginn.fdm import create_fdmexec
from huginn import configuration

class TestCreateFDMExec(TestCase):
    def test_create_fdmexec(self):
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdmexec = create_fdmexec(huginn_data_path, "Rascal", configuration.DT)

        self.assertIsNotNone(fdmexec)
