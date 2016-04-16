from unittest import TestCase

from huginn import configuration
from huginn.unit_conversions import convert_feet_to_meters 
from huginn.fdm import FDMBuilder
from huginn.sensors import Accelerometer

class AccelerometerTests(TestCase):
    def test_accelerometer(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        accelerometer = Accelerometer(fdmexec)

        self.assertAlmostEqual(accelerometer.x_acceleration, convert_feet_to_meters(fdmexec.GetAuxiliary().GetPilotAccel(1)))
        self.assertAlmostEqual(accelerometer.y_acceleration, convert_feet_to_meters(fdmexec.GetAuxiliary().GetPilotAccel(2)))
        self.assertAlmostEqual(accelerometer.z_acceleration, convert_feet_to_meters(fdmexec.GetAuxiliary().GetPilotAccel(3)))
