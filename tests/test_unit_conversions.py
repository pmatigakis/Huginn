from unittest import TestCase

from huginn.unit_conversions import (convert_jsbsim_acceleration,
                                     convert_jsbsim_angular_acceleration,
                                     convert_jsbsim_angular_velocity,
                                     convert_jsbsim_velocity,
                                     convert_jsbsim_pressure,
                                     convert_jsbsim_temperature,
                                     convert_jsbsim_density,
                                     convert_jsbsim_force)

class AccelerationConversionTests(TestCase):
    def test_convert_acceleration(self):
        acceleration = 1.0
        
        expected_acceleration = 0.304799

        converted_acceleration = convert_jsbsim_acceleration(acceleration)

        self.assertAlmostEqual(converted_acceleration, expected_acceleration, 3)

    def test_convert_angular_acceleration(self):
        acceleration = 1.0
        
        expected_acceleration = 57.2958

        converted_acceleration = convert_jsbsim_angular_acceleration(acceleration)

        self.assertAlmostEqual(converted_acceleration, expected_acceleration, 3)

class VelocityConversionTests(TestCase):
    def test_convert_angular_velocity(self):
        velocity = 1.0
        
        expected_velocity = 57.2958

        converted_velocity = convert_jsbsim_angular_velocity(velocity)

        self.assertAlmostEqual(converted_velocity, expected_velocity, 3)

    def test_convert_velocity(self):
        velocity = 1.0
        
        expected_velocity = 0.3048

        converted_velocity = convert_jsbsim_velocity(velocity)

        self.assertAlmostEqual(converted_velocity, expected_velocity, 3)

class PressureConversionTests(TestCase):
    def test_convert_pressure(self):
        pressure = 1.0
        
        expected_pressure = 47.8803

        converted_pressure = convert_jsbsim_pressure(pressure)

        self.assertAlmostEqual(converted_pressure, expected_pressure, 3)

class TemperatureConversionTests(TestCase):
    def test_convert_temperature(self):
        temperature = 1.0
        
        expected_temperature = 0.555556

        converted_temperature = convert_jsbsim_temperature(temperature)

        self.assertAlmostEqual(converted_temperature, expected_temperature, 3)

class DensityConversionTests(TestCase):
    def test_convert_density(self):
        density = 1.0
        
        expected_density = 515.378819

        converted_density = convert_jsbsim_density(density)

        self.assertAlmostEqual(expected_density, converted_density, 3)

class ForceConversionTests(TestCase):
    def test_convert_force(self):
        force = 1.0
        
        expected_force = 4.44822

        converted_force = convert_jsbsim_force(force)

        self.assertAlmostEqual(expected_force, converted_force, 3)
