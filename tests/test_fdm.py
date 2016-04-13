import math
from unittest import TestCase

from huginn.fdm import FDMBuilder, Accelerations, FDM, Velocities
from huginn import configuration
from huginn.unit_conversions import convert_feet_to_meters

#here are defined the accelerations when the JSBSim model is at the initial
#conditions
ic_x_acceleration = convert_feet_to_meters(-7.829086)
ic_y_acceleration = convert_feet_to_meters(0.985110)
ic_z_acceleration = convert_feet_to_meters(-26.564349)

ic_roll_rate = math.degrees(0.020975) 
ic_pitch_rate = math.degrees(-0.056170)
ic_yaw_rate = math.degrees(0.019293)

class TestCreateFDMExec(TestCase):
    def test_create_fdmexec(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm = fdm_builder.create_fdm()

        self.assertIsNotNone(fdm)

class AccelerationsTests(TestCase):
    def test_accelerations(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        accelerations = Accelerations(fdmexec)

        self.assertAlmostEqual(accelerations.x, ic_x_acceleration, 3)
        self.assertAlmostEqual(accelerations.y, ic_y_acceleration, 3)
        self.assertAlmostEqual(accelerations.z, ic_z_acceleration, 3)

class FDMTests(TestCase):
    def setUp(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        self.fdmexec = fdm_builder.create_fdm()
    
    def test_fdm_accelerations(self):
        fdm = FDM(self.fdmexec)

        self.assertAlmostEqual(fdm.accelerations.x, ic_x_acceleration, 3)
        self.assertAlmostEqual(fdm.accelerations.y, ic_y_acceleration, 3)
        self.assertAlmostEqual(fdm.accelerations.z, ic_z_acceleration, 3)

    def test_velocities(self):
        fdm = FDM(self.fdmexec)

        self.assertAlmostEqual(fdm.velocities.roll_rate, ic_roll_rate, 3)
        self.assertAlmostEqual(fdm.velocities.pitch_rate, ic_pitch_rate, 3)
        self.assertAlmostEqual(fdm.velocities.yaw_rate, ic_yaw_rate, 3)

class VelocitiesTests(TestCase):
    def test_accelerations(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        velocities = Velocities(fdmexec)

        self.assertAlmostEqual(velocities.roll_rate, ic_roll_rate, 3)
        self.assertAlmostEqual(velocities.pitch_rate, ic_pitch_rate, 3)
        self.assertAlmostEqual(velocities.yaw_rate, ic_yaw_rate, 3)
