import math
from unittest import TestCase

from huginn import configuration
from huginn.unit_conversions import convert_feet_to_meters, convert_rankine_to_kelvin
from huginn.fdm import FDMBuilder
from huginn.sensors import Sensors, Accelerometer, Gyroscope, Thermometer

class AccelerometerTests(TestCase):
    def test_accelerometer(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        accelerometer = Accelerometer(fdmexec)

        self.assertAlmostEqual(accelerometer.x, convert_feet_to_meters(fdmexec.GetAuxiliary().GetPilotAccel(1)))
        self.assertAlmostEqual(accelerometer.y, convert_feet_to_meters(fdmexec.GetAuxiliary().GetPilotAccel(2)))
        self.assertAlmostEqual(accelerometer.z, convert_feet_to_meters(fdmexec.GetAuxiliary().GetPilotAccel(3)))

class GyroscopeTests(TestCase):
    def test_gyroscope(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        gyroscope = Gyroscope(fdmexec)

        self.assertAlmostEqual(gyroscope.roll_rate, math.degrees(fdmexec.GetAuxiliary().GetEulerRates(1)))
        self.assertAlmostEqual(gyroscope.pitch_rate, math.degrees(fdmexec.GetAuxiliary().GetEulerRates(2)))
        self.assertAlmostEqual(gyroscope.yaw_rate, math.degrees(fdmexec.GetAuxiliary().GetEulerRates(3)))

class ThermometerTests(TestCase):
    def test_thermometer(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        thermometer = Thermometer(fdmexec)

        self.assertAlmostEqual(thermometer.temperature, convert_rankine_to_kelvin(fdmexec.GetAtmosphere().GetTemperature()))

class SensorTests(TestCase):
    def test_accelerometer(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        sensors = Sensors(fdmexec)

        self.assertAlmostEqual(sensors.accelerometer.x, convert_feet_to_meters(fdmexec.GetAuxiliary().GetPilotAccel(1)))
        self.assertAlmostEqual(sensors.accelerometer.y, convert_feet_to_meters(fdmexec.GetAuxiliary().GetPilotAccel(2)))
        self.assertAlmostEqual(sensors.accelerometer.z, convert_feet_to_meters(fdmexec.GetAuxiliary().GetPilotAccel(3)))

    def test_gyroscope(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        sensors = Sensors(fdmexec)

        self.assertAlmostEqual(sensors.gyroscope.roll_rate, math.degrees(fdmexec.GetAuxiliary().GetEulerRates(1)))
        self.assertAlmostEqual(sensors.gyroscope.pitch_rate, math.degrees(fdmexec.GetAuxiliary().GetEulerRates(2)))
        self.assertAlmostEqual(sensors.gyroscope.yaw_rate, math.degrees(fdmexec.GetAuxiliary().GetEulerRates(3)))

    def test_thermometer(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        sensors = Sensors(fdmexec)

        self.assertAlmostEqual(sensors.thermometer.temperature, convert_rankine_to_kelvin(fdmexec.GetAtmosphere().GetTemperature()))
