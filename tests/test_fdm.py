from unittest import TestCase
import inspect
from os import path

import huginn
from huginn.fdm import create_fdmexec
from huginn import configuration

class TestCreateFDMExec(TestCase):
    def test_create_fdmexec(self):
        huginn_path = inspect.getfile(huginn)
        huginn_data_path = path.join(path.dirname(huginn_path), "data")

        fdmexec = create_fdmexec(huginn_data_path, "Rascal", configuration.DT)

        self.assertIsNotNone(fdmexec)
