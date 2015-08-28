from unittest import TestCase

from huginn.unit_conversions import convert_feet_to_meters, convert_knots_to_meters_per_sec
from huginn.unit_conversions import convert_feet_sec_squared_to_meters_sec_squared, convert_radians_sec_to_degrees_sec
from huginn.unit_conversions import convert_rankine_to_kelvin, convert_psf_to_pascal

class TestConvertFeetToMeters(TestCase):
    def test_convert_feet_to_meters(self):
        feet = 10.0
        
        meters = convert_feet_to_meters(feet)
        
        expected_meters = 3.048
        
        self.assertAlmostEqual(meters, expected_meters, 3)
        
class TestConvertKnotsToMetersPerSec(TestCase):
    def test_convert_knots_to_meters_per_sec(self):
        knots = 15.0
        
        meters_per_sec = convert_knots_to_meters_per_sec(knots)
        
        expected_meters_per_sec = 7.71667
        
        self.assertAlmostEqual(meters_per_sec, expected_meters_per_sec, 3)
        
class TestConvertFeetPerSecondSquaredToMetersPerSecondSquared(TestCase):
    def test_convert_feet_sec_squared_to_meters_sec_squared(self):
        feet_sec_squared = 5.0
        
        meters_sec_squared = convert_feet_sec_squared_to_meters_sec_squared(feet_sec_squared)
        
        expected_meters_sec_squared = 1.524
        
        self.assertAlmostEqual(meters_sec_squared, expected_meters_sec_squared, 3)
        
class TestConvertRadiansPerSecondToDegreesPerSecond(TestCase):
    def test_convert_radians_sec_to_degrees_sec(self):
        radians_sec = 0.5
        
        degrees_sec = convert_radians_sec_to_degrees_sec(radians_sec)
        
        expected_degrees_sec = 28.6478
        
        self.assertAlmostEqual(degrees_sec, expected_degrees_sec, 3)
        
class TestConvertRankineToKelvin(TestCase):
    def test_convert_rankine_to_kelvin(self):
        temperature_in_rankine = 99.0
        
        temperature_in_kelvin = convert_rankine_to_kelvin(temperature_in_rankine)
        
        expected_temperature_in_kelvin = 55 
        
        self.assertAlmostEqual(temperature_in_kelvin, expected_temperature_in_kelvin, 3)
        
class TestConvertPSFToPascal(TestCase):
    def test_convert_psf_to_pascal(self):
        pressure_in_psf = 2116.216627
        
        pressure_in_pascal = convert_psf_to_pascal(pressure_in_psf)
        
        expected_pressure_in_pascal = 101325.0
        
        self.assertAlmostEqual(pressure_in_pascal, expected_pressure_in_pascal, 3)