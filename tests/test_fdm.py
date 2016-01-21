import pkg_resources
from unittest import TestCase

from huginn.fdm import FDMBuilder
from huginn import configuration

class TestCreateFDMExec(TestCase):
    def test_create_fdmexec(self):
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm = fdm_builder.create_fdm()

        self.assertIsNotNone(fdm)
